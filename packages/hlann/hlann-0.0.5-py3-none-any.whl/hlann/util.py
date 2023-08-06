#
# Copyright (c) 2023 Be The Match.
#
# This file is part of HLA-DB 
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
import re
from typing import Union, Dict, List
import json
from collections import defaultdict

def get_two_field_allele(allele_name : str) -> str:
    """
    Obtains allele name with only first two fields
    """
    return ':'.join(str(allele_name).split(':')[:2])

def calc_hla_class(locus : str) -> int:
    """
    Calculate the HLA class of this particular allele typing.
    """
    if locus in ['A', 'C','B']:
        return 1
    elif 'D' in locus:
        return 2
    else:
        raise Exception(locus,
        "Check this locus. Cannot determine its HLA class")

def sort_df(df : pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    df_headers = pd.core.frame.DataFrame([[float(val) for val in 
                                            re.sub(r'[A-Z]$', '.5', re.sub(r'.+\*', '', name)).split(':')]
                                 for name in df.index], index=df.index)
    df_headers = df_headers.sort_values(list(df_headers.columns))
    return df.loc[df_headers.index]

def combine_dict_lists(dict1 : Dict[any, list], dict2 : Dict[any, list]) -> Dict[any, list]:
    result = defaultdict(list)
    for d in [dict1, dict2]:
        for k, v in d.items():
            result[k].append(v)
    return dict(result)

def flatten_dict(annotation : Union[str, Dict[str, any]], prefix : str = "",
        exceptions : List[str] = []) -> Dict[str, str]:
    if isinstance(annotation, str):
        return {prefix : annotation}
    elif isinstance(annotation, dict):
        ann_items = annotation.items()  
    elif isinstance(annotation, list):
        return {prefix : json.dumps(annotation)}
    elif isinstance(annotation, bool):
        return {prefix : annotation}
    elif isinstance(annotation, int):
        return {prefix : annotation}
    elif annotation == None:
        return {prefix : None}
    else:
        ann_items = annotation.serialize().items()
    annotation_flat = {}
    for k, v in ann_items:
        if k not in ['alleles_hi_res', 'seq_diffs']:
            if k in exceptions:
            # print(annotation_flat, flatten_dict(v, prefix=k), type(v))
                annotation_flat[k] = flatten_dict(v, prefix=prefix)
            else:
                if prefix:
                    prefix = (prefix + '_').replace('__', '_')
                annotation_flat.update(flatten_dict(v, prefix=prefix + k))
    return annotation_flat