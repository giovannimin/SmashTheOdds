# -*- coding: utf-8 -*-
"""
Created on 25/05/2023 20:32
@author: GiovanniMINGHELLI
"""

from sources.preprocessor import make_table
from sources.api_connect import project_path
import os

if __name__ == '__main__':
    table = make_table(n=200)
    table.to_csv(os.path.join(project_path, 'database.nosync', 'updated_table.csv'))
