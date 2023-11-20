from dotenv import dotenv_values


class EnvReader:
    def __init__(self):
        self.env = dotenv_values(".env")
        self.domain = self.env["DOMAIN"]
        self.api_secret = self.env["API_SECRET"]
        self.shopper_id = self.env["SHOPPER_ID"]
        self.api_key = self.env["API_KEY"]
        self.excluded_records = self.env["EXCLUDED_RECORDS"].split(",")
