from EnvReader import EnvReader
from IpChecker import get_dns_records
import requests


def remove_excluded_records(records, env):
    excluded_records = env.excluded_records
    return [record["name"] for record in records if record["name"] not in excluded_records]


def update(record, new_ip, env):
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

    response = requests.request("PUT", url, json=payload, headers=headers)

    print(response.text)


def update_records(new_ip):
    env = EnvReader()
    dns_records = remove_excluded_records(get_dns_records(), env)

    for record in dns_records:
        update(record, new_ip, env)
