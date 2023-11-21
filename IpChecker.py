import re

from requests import get
import requests
import json
import ipaddress
from EnvReader import EnvReader
import logging
from Logger import Logger

logger = Logger()


def find_current_ip_address():
    try:
        external_ip = get('https://api.ipify.org').content.decode('utf8')
    except (Exception,) as e:
        logger.print_and_log(
            "Failed to retrieve your public ip address" + e,
            logging.WARNING
        )
        exit(-1)

    return ipaddress.IPv4Address(external_ip)


def get_dns_records():
    env = EnvReader()

    url = f"https://api.godaddy.com/v1/domains/{env.domain}/records/A"

    payload = ""
    headers = {
        "accept": "application/json",
        "X-Shopper-Id": f"{env.shopper_id}",
        "Authorization": f"sso-key {env.api_key}:{env.api_secret}"
    }

    try:
        req = requests.request("GET", url, data=payload, headers=headers).text
    except (Exception,) as e:
        logger.print_and_log(
            "Failed to retrieve your dns records" + e,
            logging.WARNING
        )
        exit(-1)

    return json.loads(req)


def find_godaddy_ip():
    dns_records = get_dns_records()
    # Define a regular expression to match an IPv4 address
    ip_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

    # Iterate through the records
    for record in dns_records:
        match = ip_regex.search(record["data"])
        if match:
            return ipaddress.IPv4Address(match.group())

    logger.print_and_log("No IP address could be retrieved from GODADDY")
    exit(-1)


def is_same(ip_a, ip_b):
    return ip_a == ip_b
