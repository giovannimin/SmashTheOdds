# -*- coding: utf-8 -*-
"""
Created on 24/05/2023 15:04
@author: GiovanniMINGHELLI
"""
import base64
import pytest
from sources.get_data import Tennis


class TestTennisAPI:
    @pytest.fixture(scope='class')
    def api(self):
        with open("token.txt", "r") as file:
            token = base64.b64decode(file.read()).decode()
        return Tennis(api_key=token)

    @pytest.mark.parametrize('year, month, day', [(2023, 5, 23), (2023, 5, 24), (2023, 5, 25)])
    def test_daily_results(self, api, year, month, day):
        assert api.get_daily_results(year=year, month=month, day=day).status_code == 200

    @pytest.mark.parametrize('year, month, day', [(2023, 5, 23), (2023, 5, 24), (2023, 5, 25)])
    def test_daily_schedule(self, api, year, month, day):
        assert api.get_daily_schedule(year=year, month=month, day=day).status_code == 200

    def test_competition(self, api):
        assert api.get_competition().status_code == 200

    def test_match_proba(self, api):
        assert api.get_match_proba(match_id=9734443).status_code == 200
        assert api.get_match_proba(match_id=1234).status_code == 404

    def test_match_summary(self, api):
        assert api.get_match_summary(match_id=9734443).status_code == 200
        assert api.get_match_summary(match_id=1234).status_code == 404

    def test_match_timeline(self, api):
        assert api.get_match_timeline(match_id=9734443).status_code == 200
        assert api.get_match_timeline(match_id=1234).status_code == 404

    def test_head_to_head(self, api):
        assert api.get_head_to_head(player1_id=407573, player2_id=163504).status_code == 200
        assert api.get_head_to_head(player1_id=1234, player2_id=4567).status_code == 404

    def test_player_profile(self, api):
        assert api.get_player_profile(player_id=163504).status_code == 200
        assert api.get_player_profile(player_id=1234).status_code == 404

    def test_race_ranking(self, api):
        assert api.get_race_ranking().status_code == 200

    def test_ranking(self, api):
        assert api.get_ranking().status_code == 200

    def test_player_result(self, api):
        assert api.get_player_result(player_id=163504).status_code == 200
        assert api.get_player_result(player_id=1234).status_code == 404

    def test_player_schedule(self, api):
        assert api.get_player_schedule(player_id=163504).status_code == 200
        assert api.get_player_schedule(player_id=1234).status_code == 404
