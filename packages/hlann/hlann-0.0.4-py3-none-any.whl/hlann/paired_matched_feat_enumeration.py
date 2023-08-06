#
# Copyright (c) 2023 Be The Match.
#
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
from .allotype import Allotype
from typing import Dict, List, Tuple
from .sequence_match import SeqMatch
from .snp import Snp
from .matched_feat_enumeration import MatchedFeatEnumeration
from collections import defaultdict
from .util import combine_dict_lists

class PairedMatchedFeatEnumeration(object):

    def __init__(self, 
            mfe_one : MatchedFeatEnumeration,
            mfe_two : MatchedFeatEnumeration) -> None:
        self.mfe_one = mfe_one
        self.mfe_two = mfe_two

        self.mfe_nt = self.mfe_aa = None
        self.num_diff_nt = self.num_diff_aa = 0
        self.num_diff_nt_ard = self.num_diff_aa_ard = 0
        self.snps_nt = {}
        self.snps_aa = {}
        self._parse_data()

    def _parse_data(self) -> None:
        self.mfe_nt = self.mfe_one.mfe_nt + ':' + self.mfe_two.mfe_nt
        self.mfe_aa = self.mfe_one.mfe_aa + ':' + self.mfe_two.mfe_aa
        self.num_diff_nt = self.mfe_one.num_diff_nt + self.mfe_two.num_diff_nt
        self.num_diff_aa = self.mfe_one.num_diff_aa + self.mfe_two.num_diff_aa
        self.num_diff_nt_ard = self.mfe_one.num_diff_nt_ard + self.mfe_two.num_diff_nt_ard
        self.num_diff_aa_ard = self.mfe_one.num_diff_aa_ard + self.mfe_two.num_diff_aa_ard
        # snp_dict = defaultdict(list)
        # for snps in [self.mfe_one.snps, self.mfe_two.snps]:
        #     for feat_name, snp_list in snps.items():
        #         snp_dict[feat_name].append(snp_list)
        self.snps_nt = combine_dict_lists(self.mfe_one.snps_nt, self.mfe_two.snps_nt)
        self.snps_aa = combine_dict_lists(self.mfe_one.snps_aa, self.mfe_two.snps_aa)

    def serialize(self) -> Dict[str, any]:
        serialization = {'mfe_nt' : self.mfe_nt,
                    'mfe_aa' : self.mfe_aa,
                    'num_diff_nt' : self.num_diff_nt,
                    'num_diff_aa' : self.num_diff_aa,
                    'num_diff_nt_ard' : self.num_diff_nt_ard,
                    'num_diff_aa_ard' : self.num_diff_aa_ard,
                    'snps_nt' : {feat : [[str(snp) for snp in snps] for snps in snp_list]
                                         for feat, snp_list in self.snps_nt.items()},
                    'snps_aa' : self.snps_aa}
        return serialization

    def __add__(self, mfe2 : any) -> any:
        self.mfe_nt + mfe2.mfe_nt