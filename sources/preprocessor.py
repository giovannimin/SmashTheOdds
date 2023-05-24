# -*- coding: utf-8 -*-
"""
Created on 24/05/2023 22:07
@author: GiovanniMINGHELLI
"""
import pandas as pd
from datetime import date
from sources.get_data import Tennis


def prep_daily_results():
    today = date.today()
    Tennis().get_daily_results(year=today.year, month=today.month, day=today.day)


def get_daily_schedule():
    today = date.today()
    Tennis().get_daily_schedule(year=today.year, month=today.month, day=today.day)


def prep_competition() -> pd.DataFrame:
    data = Tennis().get_competition().json()['tournaments']
    data = pd.DataFrame(data).drop('sport', axis=1)
    data = pd.concat([data, data['current_season'].apply(pd.Series), data['category'].apply(pd.Series)], axis=1)
    data.drop(['current_season', 'category'], axis=1, inplace=True)
    return data
