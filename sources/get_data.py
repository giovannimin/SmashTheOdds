# -*- coding: utf-8 -*-
"""
Created on 23/05/2023 18:31
@author: GiovanniMINGHELLI
"""

from sources.api_connect import API


class Tennis(API):
    def __init__(self, api_key: str, format_: str = 'json', access_level: str = 'trial',
                 version: str = 'v2', language_code: str = 'fr', timeout: int = 5, sleep_time: float = 1.5):
        super().__init__(api_key, format_, access_level, version, language_code, timeout, sleep_time)

    def get_daily_results(self, year: int, month: int, day: int):
        """Provides match information and scoring, for all matches played on a given day"""
        return self._make_request(path=f'/schedules/{year}-{str(month).zfill(2)}-{str(day).zfill(2)}/results')


    def get_competition(self):
        return self._make_request(path=f'/tournaments')



test = Tennis('r53hybpurp6agtenfp2qfpmr').get_daily_results(2023, 4, 2)


#%%
