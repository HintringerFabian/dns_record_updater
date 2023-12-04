import logging
from datetime import datetime


class Logger:
    def __init__(self, log_file: str = "dns_record_updater.log") -> None:
        """
        Initializes the Logger class with an optional log file name.
        It configures the logging module to write log messages to the specified file.

        Args:
            log_file (str, optional): The name of the log file. Defaults to "dns_record_updater.log".
        """
        logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w")

    def print_and_log(self, log_msg: str, log_level: int = logging.INFO) -> None:
        """
        Prints and logs the given log_msg with an optional log level.
        It adds a timestamp to the log statement and uses the logging module to write the log message to the file.

        Args:
            log_msg (str): The log message to be printed and logged.
            log_level (int, optional): The log level. Defaults to logging.INFO.
        """
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        log_statement = f"{timestamp} {log_msg}"
        print(log_statement)
        logging.log(log_level, log_statement)
