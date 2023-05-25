# -*- coding: utf-8 -*-
"""
Created on 25/05/2023 17:09
@author: GiovanniMINGHELLI
"""

import re



def get_number_in_id(sr_id: str) -> str:
    """
    IDs are encoded in Tennis API like (sr:competitor:983784, sr:tournament:87389, etc.)
    Returns the ID without the prefix.
    :param sr_id: (str) Encoded ID.
    :return: (str) ID without prefix.
    """
    numbers = re.findall(r'\d+', sr_id)
    return numbers[0] if numbers else ""
