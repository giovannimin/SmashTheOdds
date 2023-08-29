# -*- coding: utf-8 -*-
"""
Created on 27/07/2023 15:37
@author: GiovanniMINGHELLI
"""

from datetime import datetime
import os
from typing import List
import pytest
import requests

api_url = os.getenv("API_URL")
if not api_url:
    api_url = 'http://localhost:8000'

log_path = os.getenv("LOG_PATH")
if not log_path:
    log_path = 'SmashTheOdds/logs/logs.txt'


@pytest.mark.parametrize(
    "route, expected_status, params",
    [
        (["status"], 200, {}),
        (["predict"], 200, {'match_id': 42024053}),
        (["predict"], 200, {'match_id': 1}),
    ],
)
def test_api(route: List[str], expected_status: int, params: dict):
    """
    :param route:
    :param expected_status:
    :param params:
    :return:
    """
    def url_maker(endpoint: List[str] = None, api: str = api_url):
        """
        :param endpoint:
        :param api:
        :return:
        """
        if endpoint:
            return f'{api}/{"/".join(endpoint)}'
        return f'{api}'

    session = requests.Session()
    url = url_maker(route)
    response = session.get(url=url, params=params)

    with open(log_path, 'a') as file:
        file.write(f"""
    _________________________________________________________
    > {datetime.now()}
    > request done at {url}
        | params = "{params}"
        | status = "{response.status_code}"
        | object = "{response.json()}"
    _________________________________________________________\n
    """)

    assert response.status_code == expected_status

