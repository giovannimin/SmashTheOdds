# -*- coding: utf-8 -*-
"""
Created on 25/05/2023 20:32
@author: GiovanniMINGHELLI
"""

import os

from ..data_pipeline.preprocessing.preprocessor import make_table
from ..utils.utils import get_root

if __name__ == '__main__':
    project_path = get_root()
    table = make_table(n=200)
    table.to_csv(os.path.join(project_path, 'database.nosync', 'updated_table.csv'),  mode='a', header=False,
                 index=False)

