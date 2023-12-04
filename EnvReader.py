import re

from dotenv import dotenv_values


class EnvReader:
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"

    @staticmethod
    def __prepare_record(input_string: str) -> str:
        # Use regular expression to replace whitespaces, newlines, and tabs with an empty string
        pattern = re.compile(r'\s+')
        result = re.sub(pattern, '', input_string)
        return result

    def __init__(self):
        self.env = dotenv_values(".env")
        self.domain = self.env["DOMAIN"]
        self.api_secret = self.env["API_SECRET"]
        self.shopper_id = self.env["SHOPPER_ID"]
        self.api_key = self.env["API_KEY"]
        self.dns_records = [self.__prepare_record(record) for record in self.env["DNS_RECORDS"].split(",")]

        self.mode = self.env.get("MODE", self.INCLUDE)

        if self.mode not in {self.INCLUDE, self.EXCLUDE}:
            self.mode = self.INCLUDE
