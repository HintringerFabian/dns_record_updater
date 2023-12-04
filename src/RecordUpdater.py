import asyncio
import ipaddress
import logging

import requests

from src.EnvReader import EnvReader
from src.IpChecker import get_dns_records
from src.Logger import Logger

logger = Logger()


def remove_excluded_records(records: list, env: EnvReader) -> set:
    """
    Removes the excluded DNS records from a list of records based on the provided environment settings.

    Args:
    - records (list): A list of DNS records, where each record is a dictionary with a "name" key.
    - env (EnvReader): An instance of the `EnvReader` class that contains the environment settings.

    Returns:
    - result (list): A list of DNS records that are not excluded based on the environment settings.
    """

    excluded_records = set(env.dns_records)
    return {record.get("name") for record in records if record.get("name") not in excluded_records}


def include_records(dns_records: list, env: EnvReader) -> set:
    """
    Filters a list of DNS records based on the included records specified in the environment settings.

    Args:
        dns_records (list): A list of DNS records, where each record is a dictionary with a "name" key.
        env (EnvReader): An instance of the `EnvReader` class that contains the environment settings.

    Returns:
        set: A list of DNS records that are included based on the environment settings. Each record is represented
        by its "name" value.
    """
    included_records = set(env.dns_records)
    return {record.get("name") for record in dns_records if record.get("name") in included_records}


async def update(record: str, new_ip: ipaddress.IPv4Address, env: EnvReader) -> None:
    """
    Update a DNS record with a new IP address using the GoDaddy API.

    Args:
        record (str): The name of the DNS record to be updated.
        new_ip (str): The new IP address to be set for the DNS record.
        env (EnvReader): An object that provides access to environment variables.

    Returns:
        None: The function does not return any value.
        The result of the update operation is logged using the `Logger` class.
    """
    url = f"https://api.godaddy.com/v1/domains/{env.domain}/records/A/{record}"

    payload = [
        {
            "data": new_ip,
            "ttl": 3600
        }
    ]
    headers = {
        "accept": "application/json",
        "X-Shopper-Id": env.shopper_id,
        "Content-Type": "application/json",
        "Authorization": f"sso-key {env.api_key}:{env.api_secret}"
    }

    failed = False
    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        failed = True
        logger.print_and_log(f"Was not able to change the ip of record: {record}\n {e}", logging.WARNING)

    if not failed:
        logger.print_and_log(f"DNS record {record} now has the ip address {new_ip}")


def filter_records(dns_records: list, env: EnvReader) -> set:
    """
    Filters a list of DNS records based on the mode specified in the environment settings.

    Args:
        dns_records (list): A list of DNS records, where each record is a dictionary with a "name" key.
        env (EnvReader): An instance of the `EnvReader` class that contains the environment settings.

    Returns:
        set: A set of DNS records that are filtered based on the mode specified in the environment settings.
             Each record is represented by its "name" value.
    """
    if not isinstance(dns_records, list):
        raise TypeError("dns_records must be a list")
    if not isinstance(env, EnvReader):
        raise TypeError("env must be an instance of EnvReader")

    mode = env.mode

    if mode == EnvReader.INCLUDE:
        return include_records(dns_records, env)
    elif mode == EnvReader.EXCLUDE:
        return remove_excluded_records(dns_records, env)


async def update_records(new_ip: ipaddress.IPv4Address) -> None:
    """
    Updates DNS records with a new IP address using the GoDaddy API.

    Args:
        new_ip (str): The new IP address to be set for the DNS records.

    Returns:
        None: The function updates the DNS records with the new IP address.
    """
    dns_records_task = get_dns_records()
    env = EnvReader()
    filtered_records = filter_records(await dns_records_task, env)

    await_updates = [update(record, new_ip, env) for record in filtered_records]
    await asyncio.gather(*await_updates)
