import logging
from datetime import datetime


class Logger:
    def __init__(self, log_file="dns_record_updater.log"):
        logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w")

    @staticmethod
    def print_and_log(log_msg, log_level=logging.INFO):
        # Get the current timestamp in the specified format
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # Construct the log statement with timestamp
        log_statement = f"{timestamp} {log_msg}"

        # Print and log the statement
        print(log_statement)
        logging.log(log_level, log_statement)
