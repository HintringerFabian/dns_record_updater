from typing import List
import re

from dotenv import dotenv_values


class EnvReader:
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"

    @staticmethod
    def __prepare_record(input_string: str) -> str:
        """
        Private static method that takes an input string and uses regular expressions to remove whitespace,
        newline, and tab characters.
        It returns the cleaned up string.
        """
        pattern = re.compile(r'\s+')
        result = re.sub(pattern, '', input_string)
        return result

    @staticmethod
    def __split_dns_record(record: str) -> List[str]:
        """
        Private method that takes a DNS record and splits it by the comma into a list of strings.
        """
        if not isinstance(record, str):
            return []
        elif not record.strip():
            return []
        else:
            split_records = record.split(",")
            return [record for record in split_records if record.strip()]

    def __prepare_dns_records(self, dns_records: str) -> List[str]:
        """
        Private method that takes a comma-separated string of DNS records and cleans them up by removing whitespace,
        newline, and tab characters.
        It returns a list of cleaned up DNS records.
        """
        split_records = self.__split_dns_record(dns_records)
        return [self.__prepare_record(record) for record in split_records]

    def __validate_mode(self):
        """
        Private method that validates the mode field and sets it to the default value if it is not a valid mode.
        """
        if self.mode not in {self.INCLUDE, self.EXCLUDE}:
            self.mode = self.INCLUDE

    def __init__(self):
        """
        Initializes the EnvReader class by loading environment variables
        from the .env file and setting the corresponding fields.
        """
        self.env = dotenv_values("../.env")
        self.domain = self.env["DOMAIN"]
        self.api_secret = self.env["API_SECRET"]
        self.shopper_id = self.env["SHOPPER_ID"]
        self.api_key = self.env["API_KEY"]
        self.dns_records = self.__prepare_dns_records(self.env["DNS_RECORDS"])

        self.mode = self.env.get("MODE", self.INCLUDE)
        self.__validate_mode()
