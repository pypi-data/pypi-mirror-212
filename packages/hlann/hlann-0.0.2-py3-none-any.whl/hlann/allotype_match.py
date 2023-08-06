#
# Copyright (c) 2023 Be The Match.
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
import re
from copy import deepcopy
from typing import List, Dict, Union, Tuple
from .allotype import Allotype
from .genotype import Genotype
from .ref_data import RefData
from .sequence import Sequence
from .sequence_match import SeqMatch
from .snp import Snp
from Bio.Seq import Seq
# from Bio.Alphabet import IUPAC
import editdistance
from pyard import ARD
from .matched_feat_enumeration import MatchedFeatEnumeration

class AllotypeMatch(object):
    
    def __init__(self, allele_one: Allotype, allele_two: Allotype, ref_data : RefData=None) -> None:
        """
        Represents the match status between two HLA-B alleles.

        :param allele_one: Allotype object
        :param allele_two: Allotype object
        """
        if isinstance(allele_one, str) and isinstance(allele_two, str):
            ref_data = ref_data or RefData()
            allele_one = Allotype(str(allele_one), ref_data=ref_data)
            allele_two = Allotype(str(allele_two), ref_data=ref_data)
            # raise InvalidMatchError(allele_one, allele_two, "Need to provide two Allotype objects")
        self.allele_one, self.allele_two = allele_one, allele_two
        self.allotypes = [self.allele_one, self.allele_two]
        self.locus, self.hla_class = self._calc_locus_class()
        self.match_grade, self.matched = self._get_overall_match_grade()
        self.order = ['A', 'P', 'L', 'M']
        self.score = self.order.index(self.match_grade)
        self.snps = None
        self.num_snps = None
        self.diffs = None
        self.mfe = None

    def _calc_locus_class(self) -> Tuple[str, str]:
        locus = set([self.allele_one.locus, self.allele_two.locus])
        hla_class = set([self.allele_one.hla_class, self.allele_two.hla_class])
        if len(locus) != 1:
            raise Exception("There needs to be exactly one locus in this allele match.", self.allele_one, self.allele_two)
        if len(hla_class) != 1:
            raise Exception("There needs to be exactly one locus in this allele match.", self.allele_one, self.allele_two)
        return locus.pop(), hla_class.pop()

    def _p_group_match(self, a1: Allotype, a2: Allotype) -> bool:
        """
        Checks if there are any P groups between the alleles.
        """
        p1 = a1.calc_group('p')
        p2 = a2.calc_group('p')
        return (p1 and p2) and (p1 == p2) #and 
                # (a1.resolution != 'low') and 
                # (a2.resolution != 'low'))
        # print(p1, p2)
        # if p1 and p2:
        #     return bool(len(list(set(p1) & set(p2))))
        # return False

    def _get_match_grade(self, a1 : Allotype, a2 : Allotype) -> str:
        if a1.fields[0] == a2.fields[0]:
            if a1.fields[1] and a2.fields[1]:
                if a1.fields[1] == a2.fields[1] and not (a1.wildcard and a2.wildcard):
                    return "A"
                if self._p_group_match(a1, a2):
                    return "P"
                return "L"
            return "P"
        if self._p_group_match(a1, a2):
            return "P"
        return "M"

    def _get_overall_match_grade(self) -> Tuple[str, bool]:
        """
        Evaluates the match grade between two HLA typing codes with two-field consideration.

        Returns one of the following single-letter codes:
            A - Allotype Match - matching on both fields
            P - Potential Matches - matching on first field, ambiguity on second field
            L - Allotype Mismatch - matching on first field, mismatch on second field
            M - Mismatches - mismatch on first field
        """
        a1, a2 = self.allele_one, self.allele_two
        if a1.typing == a2.typing and a1.resolution == 'high' and a2.resolution != 'high':
            a1.matched = a2.matched = True
            return 'A', True
        match_grades = set([self._get_match_grade(potential_allele_1, potential_allele_2)
            for potential_allele_1 in a1.alleles_hi_res
            for potential_allele_2 in a2.alleles_hi_res])
        if len(match_grades) == 1 and 'A' in match_grades:
            a1.matched = a2.matched = True
            return 'A', True
        else:
            if 'A' in match_grades or 'P' in match_grades:
                # a1.potent_matched = a2.potent_matched = True
                a1.matched = a2.matched = True
                return 'P', True
            elif 'L' in match_grades:
                return 'L', False
            else:
                return 'M', False

    def get_allotype_diffs(self, align_mismatches_only : bool = True) -> Tuple[Dict[str, any], Dict[str, List[Snp]]]:
        mfe = MatchedFeatEnumeration(self.allele_one, self.allele_two, hla_class=self.hla_class)
        self.mfe = mfe
        return mfe

    def __str__(self) -> str:
        return self.match_grade

    def __repr__(self):
        return "{}↔{} ({})".format(self.allele_one, 
                         self.allele_two,
                         self.match_grade)

    def serialize(self) -> Dict[str, any]:
        output = {'allele_one' : self.allele_one.typing,
                    'allele_two' : self.allele_two.typing,
                    'match_grade' : self.match_grade,
                    'diffs' : self.mfe.serialize()}
        return output

class InvalidMatchError(Exception):

    def __init__(self, genotype_one : Genotype, 
                       genotype_two : Genotype, message : str):
        self.genotype_one = genotype_one
        self.genotype_two = genotype_two
        self.message = message