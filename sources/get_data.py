# -*- coding: utf-8 -*-
"""
Created on 23/05/2023 18:31
@author: GiovanniMINGHELLI
"""

from .api_connect import API, token


class Tennis(API):
    def __init__(self, api_key: str = token, format_: str = 'json', access_level: str = 'trial',
                 version: str = 'v2', language_code: str = 'fr', timeout: int = 5, sleep_time: float = 1.5):
        super().__init__(api_key, format_, access_level, version, language_code, timeout, sleep_time)

    def get_daily_results(self, year: int, month: int, day: int):
        """Returns a list of results for all matches on a given date."""
        return self._make_request(path=f'/schedules/{year}-{str(month).zfill(2)}-{str(day).zfill(2)}/results')

    def get_daily_schedule(self, year: int, month: int, day: int):
        """Returns a schedule of matches on a given date."""
        return self._make_request(path=f'/schedules/{year}-{str(month).zfill(2)}-{str(day).zfill(2)}/schedule')

    def get_competition(self):
        """Lists all tournaments available in the API."""
        return self._make_request(path=f'/tournaments')

    def get_match_proba(self, match_id: int):
        """Provides 2-way probabilities (home team win, away team win) for a given match."""
        return self._make_request(path=f'/matches/sr:match:{match_id}/probabilities')

    def get_match_summary(self, match_id: int):
        """Returns information for a match including live updates and statistics"""
        return self._make_request(path=f'/matches/sr:match:{match_id}/summary')

    def get_match_timeline(self, match_id: int):
        """
        Returns information for a given match ID including a timeline of events,
        (point-by-point or Game-by-Game depending on the coverage) and some basic stats
        :param match_id:
        :return:
        """
        return self._make_request(path=f'/matches/sr:match:{match_id}/timeline')

    def get_head_to_head(self, player1_id: int, player2_id: int):
        """
        Provides past and upcoming match details between two singles players given two competitor IDs
        :param player1_id:
        :param player2_id:
        :return:
        """
        return self._make_request(path=f'/players/sr:competitor:{player1_id}/versus/sr:competitor:{player2_id}/matches')

    def get_player_profile(self, player_id: int):
        """
        Provides stats and information for a given player.
        :param player_id:
        :return:
        """
        return self._make_request(path=f'/players/sr:competitor:{player_id}/profile')

    def get_race_ranking(self):
        """
        Returns a list in ascending order for the race to the ATP/WTA finals.
        :return:
        """
        return self._make_request(path=f'/players/race_rankings')

    def get_ranking(self):
        """
        Returns a list in ascending order of ATP/WTA world rankings.
        :return:
        """
        return self._make_request(path=f'/players/rankings')

    def get_player_result(self, player_id: int):
        """
        Returns a listing of results given a single player ID.
        :param player_id:
        :return:
        """
        return self._make_request(path=f'/players/sr:competitor:{player_id}/results')

    def get_player_schedule(self, player_id: int):
        """
        Returns a schedule of upcoming matches for a given player ID.
        :param player_id:
        :return:
        """
        return self._make_request(path=f'/players/sr:competitor:{player_id}/schedule')

