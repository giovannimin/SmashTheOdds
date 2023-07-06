# -*- coding: utf-8 -*-
"""
Created on 25/05/2023 20:32
@author: GiovanniMINGHELLI
"""

from preprocessor import make_table
from utils import get_root
import os

if __name__ == '__main__':
    project_path = get_root()
    table = make_table(n=200)
    table.to_csv(os.path.join(project_path, 'database.nosync', 'updated_table.csv'),  mode='a', header=False,
                 index=False)

