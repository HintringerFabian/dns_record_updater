import asyncio
import logging
from src import IpChecker
import RecordUpdater
import sys

from src.Logger import Logger
logger = Logger()


async def run_update():
    current_ip, godaddy_ip = await asyncio.gather(
        IpChecker.find_current_ip_address(),
        IpChecker.find_godaddy_ip()
    )

    if IpChecker.is_same(godaddy_ip, current_ip):
        logger.print_and_log("The ip did not change, no record will be updated")
        exit()

    await RecordUpdater.update_records(current_ip)
    # logger.print_and_log("Would have run perfectly fine, but you are in test mode.")
    exit()


def print_help():
    print("Usage: python3 main.py [-h || --help]")
    print("You need to fill the values in the .env file.")
    print("Have a look at the comments in the .env.example file to get a quick overview")
    print("or have a look through the README.md file to get a in depth description")


async def handle_args():
    arg_count = len(sys.argv) - 1
    args = sys.argv[1:]

    if arg_count == 0:
        await run_update()
        exit()
    elif arg_count > 1:
        logger.print_and_log(
            "The maximum amount of arguments allowed is 1.\n" +
            f"But you provided {arg_count} arguments: {args}",
            logging.WARNING
        )
        exit(-1)

    argument = args[0]

    match argument:
        case "-h":
            print_help()
        case "--help":
            print_help()

    exit()


if __name__ == "__main__":
    asyncio.run(handle_args())