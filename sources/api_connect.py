# -*- coding: utf-8 -*-
"""
Created on 23/05/2023 14:30
@author: GiovanniMINGHELLI
"""
import base64
import time
import requests
from sources.utils import get_root



_ = get_root()

with open("token.txt", "r") as file:
    token = base64.b64decode(file.read()).decode()


class API(object):
    session = requests.Session()

    def __init__(self, api_key: str = token, format_: str = 'json', access_level: str = 'trial',
                 version: str = 'v2', language_code: str = 'fr', timeout: int = 5, sleep_time: float = 1.5):
        """ Sportradar API Constructor

        :param api_key: key provided by Sportradar, specific to the sport's API
        :param format_: response format to request from the API (json, xml)
        :param timeout: time before quitting on response (seconds)
        :param sleep_time: time to wait between requests, (free min is 1 second)
        """

        self.api_key = api_key
        self.access_level = access_level
        self.version = version
        self.language = language_code
        self.api_root = 'https://api.sportradar.com/tennis/'
        self.format_ = "." + format_.strip(".")
        self.timeout = timeout
        self._sleep_time = sleep_time

    def _make_request(self, path, method='GET', version=None):
        time.sleep(self._sleep_time)
        if not version:
            version = self.version
        full_uri = self.api_root + self.access_level + '/' + version + '/' + self.language + path + self.format_
        print(full_uri)
        response = self.session.request(method, full_uri, timeout=self.timeout, params={'api_key': self.api_key})
        print(response.status_code)
        return response
