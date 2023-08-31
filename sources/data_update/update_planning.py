# -*- coding: utf-8 -*-
"""
Created on 25/05/2023 20:32
@author: GiovanniMINGHELLI
"""

import os

from ..data_pipeline.preprocessing.preprocessor import get_weekly_schedule
from ..utils.utils import get_root

if __name__ == '__main__':
    project_path = get_root()
    table = get_weekly_schedule()
    table.to_csv(os.path.join(project_path, 'database.nosync', 'planning_table.csv'), index=False)
