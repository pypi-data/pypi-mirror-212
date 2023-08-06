#
# Copyright (c) 2023 Be The Match.
#
# This file is part of BLEAT 
# (see https://github.com/nmdp-bioinformatics/hla-db).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import pandas as pd
import os
from typing import List, Dict
import numpy as np

class ResPubDB(object):
    def __init__(self):
        self.directory = os.path.dirname(__file__)
        self.path = self.directory + '/data/agg-matcher-tool-publications-db.xlsx'
        self.pubs = self._load_db()

    def _load_db(self) -> pd.core.frame.DataFrame:
        return pd.read_excel(self.path)
    
    def serialize(self) -> Dict[str, List[Dict[str, any]]]:
        return self.pubs.astype(object).replace(np.nan, None).to_dict(orient='records')
