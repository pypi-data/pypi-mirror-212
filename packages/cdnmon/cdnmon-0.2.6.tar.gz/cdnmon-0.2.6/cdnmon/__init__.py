import requests
import coloredlogs, logging
from . import config

class Endpoint:
    def __init__(self, endpoint=None, access_token="", debug=False):
        # ensure access token is provided
        assert access_token != "", "access_token can not be empty string"
        self.__access_token = access_token
        # build base url
        if endpoint is not None:
            self.__base_url = f"{endpoint}/api/v1"
        else:
            self.__base_url = f"{config.settings['API_ENDPOINT']}/api/v1"
        # setup logger
        self.logger = logging.getLogger(__name__)
        if debug:
            coloredlogs.install(level='DEBUG', logger=self.logger)
        else:
            coloredlogs.install(logger=self.logger)
        # add access token to session object
        self.auth()

    def auth(self):
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {self.__access_token}"

    def list_cdns(self):
        api_endpoint = config.settings["API_ENDPOINT"]
        url = f"{self.__base_url}/provider"
        response = self.session.get(url)
        self.logger.debug(f"GET {url} {response.status_code} -> {response.text}")
        return response.json()

    def get_cdn(self, name):
        api_endpoint = config.settings["API_ENDPOINT"]
        url = f"{self.__base_url}/provider/{name}"
        response = self.session.get(url)
        self.logger.debug(f"GET {url} {response.status_code} -> {response.text}")
        return response.json()

__all__ = ["Endpoint"]