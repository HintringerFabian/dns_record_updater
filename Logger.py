import logging


class Logger:
    def __init__(self, log_file="dns_record_updater.log"):
        logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w")

    @staticmethod
    def print_and_log(log_statement, log_level=logging.INFO):
        print(log_statement)
        logging.log(log_level, log_statement)
