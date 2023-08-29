# -*- coding: utf-8 -*-
"""
Created on 25/05/2023 20:32
@author: GiovanniMINGHELLI
"""

from sources.preprocessor import get_weekly_schedule
from sources.utils import get_root
import os

if __name__ == '__main__':
    project_path = get_root()
    table = get_weekly_schedule()
    table.to_csv(os.path.join(project_path, 'database.nosync', 'planning_table.csv'), index=False)
