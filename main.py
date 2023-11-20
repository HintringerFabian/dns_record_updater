from dotenv import dotenv_values

import IpChecker
from IpChecker import find_current_ip_address

if __name__ == "__main__":
    env = dotenv_values(".env")
    current_ip = find_current_ip_address()

    if current_ip == IpChecker.failed_ip_req:
        exit(-1)

