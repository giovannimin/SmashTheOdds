# -*- coding: utf-8 -*-
"""
Created on 03/07/2023 21:19
@author: GiovanniMINGHELLI
"""

from datetime import datetime, timedelta


def get_next_seven_days():
    next_seven_days = [datetime.today() + timedelta(days=i) for i in range(7)]
    return [day.strftime('%Y-%m-%d') for day in next_seven_days]


if __name__ == '__main__':
    get_next_seven_days()
