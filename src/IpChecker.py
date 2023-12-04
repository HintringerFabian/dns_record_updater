import asyncio
import ipaddress
import logging
import re
from typing import List, Dict
from typing import Tuple

import requests
from requests.exceptions import RequestException

from src.EnvReader import EnvReader
from src.Logger import Logger

logger = Logger()


async def __find_current_ip_address() -> ipaddress.IPv4Address:
    """
    Retrieves the current public IP address of the user.

    Returns:
        ipaddress.IPv4Address: The current public IP address.

    Raises:
        RequestException: If the request to retrieve the IP address fails.
    """
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        external_ip = response.text
    except RequestException as e:
        logging.warning(f"Failed to retrieve your public ip address: {e}")
        raise RequestException("Failed to retrieve public IP address")

    return ipaddress.IPv4Address(external_ip)


async def get_dns_records() -> List[Dict[str, str]]:
    """
    Retrieves DNS records for a specific domain from the GoDaddy API.

    Returns:
        A list of DNS records in JSON format. Each record contains the name,
        type, data (IP address), and TTL (time to live).
    """
    env = EnvReader()

    url = f"https://api.godaddy.com/v1/domains/{env.domain}/records/A"

    headers = {
        "accept": "application/json",
        "X-Shopper-Id": f"{env.shopper_id}",
        "Authorization": f"sso-key {env.api_key}:{env.api_secret}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.print_and_log(
            f"Failed to retrieve your dns records: {e}",
            logging.WARNING
        )
        exit(-1)

    dns_records = response.json()
    return dns_records


async def __find_godaddy_ip() -> ipaddress.IPv4Address:
    """
    Retrieves the IP address stored in the GoDaddy DNS records.

    Returns:
        The IP address stored in the GoDaddy DNS records as an `IPv4Address` object.
    """
    dns_records = await get_dns_records()
    ip_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

    for record in dns_records:
        match = ip_regex.search(record["data"])
        if match:
            return ipaddress.IPv4Address(match.group())

    logger.print_and_log("No IP address could be retrieved from GoDaddy")
    exit(-1)


async def get_ip_addresses() -> Tuple[ipaddress.IPv4Address, ipaddress.IPv4Address]:
    """
    Retrieve the current IP address and the IP address stored in the GoDaddy DNS records.

    :return: Tuple containing the current IP address and the GoDaddy IP address
    """
    return await asyncio.gather(
        __find_current_ip_address(),
        __find_godaddy_ip()
    )


def are_same_ipv4(ip_a: ipaddress.IPv4Address, ip_b: ipaddress.IPv4Address) -> bool:
    """
    Checks if two IPv4 addresses are the same.

    Args:
        ip_a: An IPv4 address.
        ip_b: An IPv4 address.

    Returns:
        True if the two IPv4 addresses are the same, False otherwise.
    """
    if not isinstance(ip_a, ipaddress.IPv4Address) or not isinstance(ip_b, ipaddress.IPv4Address):
        raise TypeError("ip_a and ip_b must be instances of ipaddress.IPv4Address")
    if ip_a is None or ip_b is None:
        raise ValueError("ip_a and ip_b must not be None")
    if ip_a == '' or ip_b == '':
        raise ValueError("ip_a and ip_b must not be empty strings")
    return ip_a == ip_b
