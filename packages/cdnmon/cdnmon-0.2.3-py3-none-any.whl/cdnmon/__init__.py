import requests
from . import config

class Endpoint:
    def __init__(self, access_token):
        self._access_token = access_token
        self.auth()

    def auth(self):
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {self._access_token}"

    def list_cdns(self):
        api_endpoint = config.settings["API_ENDPOINT"]
        url = f"https://{api_endpoint}/api/v1/providers"
        return self.session.get(url).json()

    def find_cdn(name):
        pass
