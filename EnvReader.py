from dotenv import dotenv_values


class EnvReader:
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"

    def __init__(self):
        self.env = dotenv_values(".env")
        self.domain = self.env["DOMAIN"]
        self.api_secret = self.env["API_SECRET"]
        self.shopper_id = self.env["SHOPPER_ID"]
        self.api_key = self.env["API_KEY"]
        self.dns_records = self.env["DNS_RECORDS"].split(",")

        self.mode = self.env.get("MODE", self.INCLUDE)

        if self.mode not in {self.INCLUDE, self.EXCLUDE}:
            self.mode = self.INCLUDE
