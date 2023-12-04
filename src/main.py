import asyncio
import logging
import sys

from IpChecker import are_same_ipv4
from RecordUpdater import update_records
from src import IpChecker
from src.Logger import Logger

logger = Logger()


async def run_update() -> None:
    """
    Update the DNS records with a new IP address if the current IP address is different from the IP address
    stored in the GoDaddy DNS records.

    :return: None
    """
    current_ip, godaddy_ip = await IpChecker.get_ip_addresses()

    if are_same_ipv4(godaddy_ip, current_ip):
        logger.print_and_log("The IP did not change, no record will be updated")
        return

    await update_records(current_ip)
    logger.print_and_log("DNS records updated successfully")


def print_help():
    print("Usage: python3 main.py [-h || --help]")
    print("You need to fill the values in the .env file.")
    print("Have a look at the comments in the .env.example file to get a quick overview")
    print("or have a look through the README.md file to get a in depth description")


async def handle_args():
    """
    Handle command line arguments passed to the script.

    Returns:
        None
    """
    arg_count = len(sys.argv) - 1
    args = sys.argv[1:]

    if arg_count == 0:
        await run_update()
        exit()
    elif arg_count > 1:
        logger.print_and_log(
            f"The maximum amount of arguments allowed is 1.\n" +
            f"But you provided {arg_count} arguments: {args}",
            logging.WARNING
        )
        exit(-1)

    argument = args[0]

    if argument in ["-h", "--help"]:
        print_help()

    exit()


if __name__ == "__main__":
    asyncio.run(handle_args())
