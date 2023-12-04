import asyncio

import requests

from src.EnvReader import EnvReader
from src.IpChecker import get_dns_records
import logging
from src.Logger import Logger

logger = Logger()


def remove_excluded_records(records, env):
    excluded_records = env.dns_records
    return [record["name"] for record in records if record["name"] not in excluded_records]


def include_records(dns_records, env):
    included_records = env.dns_records
    return [record["name"] for record in dns_records if record["name"] in included_records]


async def update(record, new_ip, env):
    url = f"https://api.godaddy.com/v1/domains/{env.domain}/records/A/{record}"

    payload = [
        {
            "data": f"{new_ip}",
            "ttl": 3600
        }
    ]
    headers = {
        "accept": "application/json",
        "X-Shopper-Id": f"{env.shopper_id}",
        "Content-Type": "application/json",
        "Authorization": f"sso-key {env.api_key}:{env.api_secret}"
    }

    failed = False
    try:
        requests.request("PUT", url, json=payload, headers=headers)
    except (Exception,) as e:
        failed = True
        logger.print_and_log(f"Was not able to change the ip of record: {record}\n {e}", logging.WARNING)

    if not failed:
        logger.print_and_log(f"DNS record {record} now has the ip address {new_ip}")


def filter_records(dns_records, env):
    mode = env.mode

    if mode == EnvReader.INCLUDE:
        return include_records(dns_records, env)
    elif mode == EnvReader.EXCLUDE:
        return remove_excluded_records(dns_records, env)


async def update_records(new_ip):
    dns_records_task = get_dns_records()

    env = EnvReader()
    dns_records = await dns_records_task
    dns_records = filter_records(dns_records, env)

    await_updates = []

    for record in dns_records:
        await_updates.append(
            update(record, new_ip, env)
        )

    await asyncio.gather(*await_updates)
