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
from .allotype import Allotype
from .genotype import Genotype
from .ref_data import RefData
from .allotype_match import AllotypeMatch
from pyard import ARD
from typing import Tuple, List, Dict
from .paired_matched_feat_enumeration import PairedMatchedFeatEnumeration

class GenotypeMatch(object):

    def __init__(self, genotype_recip: Genotype, genotype_donor: Genotype, ref_data : RefData = None,
                id : str = None, #align_mismatches_only : bool = True,
                ard : ARD = None) -> None:
        """
        Represents the match status between two HLA-B genotypes as a 
        two-element list of AllotypeMatches. Also, aligns the genotypes
        with the match grades. The first genotype represents the patient/recipient while
        the second genotype represents the potential donor.

        :param genotype_recip: Genotype object
        :param genotypes_donors: List of Genotype objects
        """
        self.ref_data = ref_data
        self.ard = ard
        self.id = id
        # self.align_mismatches_only = align_mismatches_only
        if isinstance(genotype_recip, str) and isinstance(genotype_donor, str):
            self.ref_data = ref_data or RefData()
            genotype_recip = Genotype(str(genotype_recip), ref_data=self.ref_data, ard=self.ard)
            genotype_donor = Genotype(str(genotype_donor), ref_data=self.ref_data, ard=self.ard)
        self.genotype_recip = genotype_recip
        self.genotype_donor = genotype_donor
        self.genotypes = [genotype_recip, genotype_donor]
        self.locus = self._validate_locus()

        self.genotype_donor_flipped = False
        self.grade, self.allotype_matches, self.num_matches = self._get_match()
        self.allotype_mismatches = None
        self.directionality = self._determine_directionality()
        self.annotation = None
        self.rank = self.index = None
        self.diffs = None

        self.matched_alleles_pat, self.matched_alleles_don, \
             self.mismatched_alleles_pat, self.mismatched_alleles_don = self.organize_alleles()


    def _validate_locus(self) -> None:
        loci = set([self.genotype_recip.locus, self.genotype_donor.locus])
        if len(loci) == 1:
            return loci.pop()
        raise Exception('There is an appropriate amount of loci. Please include only one HLA locus.')

    def annotate(self) -> Dict[str, str]:
        """
        Annotates the match with known mismatching models.
        """
        annotation = {}
        if self.locus == 'DPB1':
            annotation['tce_match'] = self.determine_TCE_match()
            annotation['expr_match'] = self.determine_expr_match()
        elif self.locus == 'B':
            annotation['b_leader'] = self.determine_leader_match()
        if annotation:
            self.annotation = annotation
        return annotation

    def _get_match(self) -> Tuple[str, Dict[str, int], List[AllotypeMatch], int]:
        """
        Compares the allotype matches between the forward and reverse versions of the genotypes
        to get the best match grade combination, which is whatever contains the highest match grade.

        (highest) A > P > L > M (lowest)

        The match grade combination is returned with the higher grade on the second element (right-most).
        The aligned genotypes are returned as well, in accordance with the match grade combination.
        
        Returns two HLA allotype match grades:
            AA - A genotype match occurs if both allotype pairs are allele matches.
            MA - A single mismatch constitutes one allele match and one mismatch.
            MM - A double mismatch occurs when both allotype pairs are mismatches.
            PA/PP/LP/MP - A potential single/double genotype match occurs when at least one pair has a potential match.
            LA/LP/LL/ML - A single/double allele genotype mismatch occurs when at least one pair has an allele mismatch.
        """
        g1_a, g1_b = self.genotype_recip.allotypes
        g2_a, g2_b = self.genotype_donor.allotypes
        match_for = [AllotypeMatch(g1_a, g2_a, ref_data=self.ref_data), AllotypeMatch(g1_b, g2_b, ref_data=self.ref_data)]
        match_rev = [AllotypeMatch(g1_a, g2_b, ref_data=self.ref_data), AllotypeMatch(g1_b, g2_a, ref_data=self.ref_data)]

        rank_for = [match_for[0].score, match_for[1].score]
        rank_rev = [match_rev[0].score, match_rev[1].score]

        matches = match_for
        if min(rank_for) < min(rank_rev):
            match_code = str(match_for[0]) + str(match_for[1])
        elif min(rank_for) > min(rank_rev):
            # self.genotype_donor.flip()
            self.genotype_donor_flipped = True
            matches = match_rev
            match_code = str(match_rev[0]) + str(match_rev[1])
        else: #TODO: Think of examples for this. Might need to look at total score.
            match_code = str(match_for[0]) + str(match_for[1])
        num_matches = len([match for match in matches if match.matched])
        # scores = self._get_genotype_diffs(matches)
        return match_code, matches, num_matches

    def _determine_directionality(self) -> str:
        """
        Determines the directionality of a match for single mismatches.
        GvH indicates a graft-versus-host mismatch vector while
        HvG indicates a host-versus-graft mismatch vector.
        :return: Match directionality
        """
        if self.grade in ['AA', 'PP', 'PA', 'AP']:
            return None
        if (not self.genotype_recip.homozygous and not self.genotype_donor.homozygous):
            return 'bidirectional'
        elif not self.genotype_recip.homozygous and self.genotype_donor.homozygous:
            return 'GvH'
        elif self.genotype_recip.homozygous and not self.genotype_donor.homozygous:
            return 'HvG'

    def determine_TCE_match(self) -> str:
        """
        Sets the TCE (T-Cell Epitope) match category. Assumes
        TCE has been assigned in the alleles already.
        """
        if self.grade in ['AA', 'AP', 'PA', 'PP']:
            return 'Allele'
        tce_pat = [allele.get_features('tce').anns.serialize()['tce'] for allele in self.genotype_recip.allotypes]
        tce_don = [allele.get_features('tce').anns.serialize()['tce'] for allele in self.genotype_donor.allotypes]
        tce_core_pat = [allele.get_features('tce_core').anns.serialize()['tce_core'] for allele in self.genotype_recip.allotypes]
        tce_core_don = [allele.get_features('tce_core').anns.serialize()['tce_core'] for allele in self.genotype_donor.allotypes]
        tce_cores = tce_core_pat + tce_core_don
        tce_cores = ['True' in str(tce_core) for tce_core in tce_cores]
        core_match = all(tce_cores)

        tce_dp84_87_pat = [allele.get_features('DP84-87').seq_anns.serialize()['DP84-87'] for allele in self.genotype_recip.allotypes]
        tce_dp84_87_don = [allele.get_features('DP84-87').seq_anns.serialize()['DP84-87'] for allele in self.genotype_donor.allotypes]
        tce_dp84_87 = tce_dp84_87_pat + tce_dp84_87_don
        dp84_74_match = len(set(tce_dp84_87)) == 1
        
        unk_val = 'unknown'
        if (unk_val in tce_pat) or (unk_val in tce_don):
            return 'Unknown'
        if not any(tce_pat + tce_don):
            raise Exception(self.genotype_recip,
                self.genotype_donor,
                'No TCE groups are assigned. Please assign first.')
        min_tce_pat = min(tce_pat)
        min_tce_don = min(tce_don)
        
        if min_tce_pat == min_tce_don:
            prefix = 'C' if core_match else 'NC'
            suffix = 'dp84_74_match' if dp84_74_match else 'dp84_87_mism'
            return '{}_permissive_{}'.format(prefix, suffix)
        elif min_tce_pat < min_tce_don:
            return 'GvH_nonpermissive'
        else:
            return 'HvG_nonpermissive'

    def organize_alleles(self) -> Tuple[List[Allotype], List[Allotype], List[Allotype], List[Allotype]]:
        """
        Organizes alleles into four outputs:
            1: alleles that are matched in the patient.
            2: alleles that are matched in the donor.
            3: alleles that are mismatched in the patient.
            4: alleles that are mismatched in the donor.
        """
        matched_grades = ['A', 'P']
        matched_alleles_pat = [match.allele_one for match in self.allotype_matches if match.match_grade in matched_grades]
        matched_alleles_don = [match.allele_two for match in self.allotype_matches if match.match_grade in matched_grades]
        mismatched_alleles_pat = [match.allele_one for match in self.allotype_matches if match.match_grade not in matched_grades]
        mismatched_alleles_don = [match.allele_two for match in self.allotype_matches if match.match_grade not in matched_grades]
        return matched_alleles_pat, matched_alleles_don, mismatched_alleles_pat, mismatched_alleles_don

    def parse_as_str(self, el_list : List[Allotype]) -> List[str]:
        """
        Returns list of Allotype object as list of string.
        """
        return [str(el) for el in el_list]

    def determine_expr_match(self) -> str:
        """
        Determines the patient's mismatched allele's expression level.
        """
        mismatched_allele_pat_expr_level = None
        if len(self.mismatched_alleles_pat) == 1:
            mismatched_allele_pat_expr_level = self.mismatched_alleles_pat[0].get_features('expression').anns.serialize()['expression']
        # elif self.grade in ['MA', 'AM', 'MP', 'PM', 'LA', 'AL', 'LP', 'PL']:
        #     mismatched_allele_pat_expr_level = self.matched_alleles_pat[0].annotation['expression']
        if not mismatched_allele_pat_expr_level:
            if self.grade in ['AA', 'AP', 'PA', 'PP']:
                return 'matched'
            elif self.grade in ['MM', 'LM', 'ML', 'LL', 'MM']:
                return 'mismatched'
            return None
        cats = {'high' : 'unfavorable',
                'low' : 'favorable',
                'unknown' : 'unknown'}
        mismatched_allele_pat_expr_level = mismatched_allele_pat_expr_level.replace('?', '').replace('~', '')
        if mismatched_allele_pat_expr_level in cats:
            self.expr_match = cats[mismatched_allele_pat_expr_level]
        else:
            self.expr_match = mismatched_allele_pat_expr_level
        return self.expr_match

    def determine_leader_match(self) -> str:
        if self.grade in ['AA', 'AP', 'PA', 'PP']:
            return 'matched'
        elif self.grade in ['MM', 'LM', 'ML', 'LL', 'MM']:
            return 'mismatched'
        p2s = []
        for allotype in [self.mismatched_alleles_pat, self.mismatched_alleles_don, self.matched_alleles_pat]:
            if len(allotype) != 1:
                raise Exception('Check the numer of allotypes in this B-leader calculation', allotype)
            allotype = allotype[0]
            # if not allotype.feats:
            #     allotype.get_features('P2')
            p2s.append(allotype.get_features('P2').seq_anns.serialize()['P2'].replace('?', ''))
        leader_match_status = ''.join(p2s)
        self.leader_match_status = leader_match_status
        return leader_match_status

    def get_genotype_diffs(self, align_mismatches_only : bool = True) -> Dict[str, int]: #List[AllotypeMatch]:
        allotype_matches = self.allotype_matches
        # allotype_mismatches = []
        # diffs = None
        # score_nt = score_aa = score_nt_ard = score_aa_ard = 0
        mfe_one = allotype_matches[0].get_allotype_diffs(align_mismatches_only=align_mismatches_only)
        mfe_two = allotype_matches[1].get_allotype_diffs(align_mismatches_only=align_mismatches_only)
        paired_mfe = PairedMatchedFeatEnumeration(mfe_one, mfe_two)
        # diffs_geno = [allo_match.get_allotype_diffs(align_mismatches_only=align_mismatches_only).serialize()
        #                 for allo_match in allotype_matches]
        self.diffs = paired_mfe
        return paired_mfe

        # diffs = {}
        # keys = [diffs_allo for diffs_allo in diffs_geno if diffs_allo]
        # scores = None
        # if keys:
        #     keys = keys[0].keys()
        #     for k in keys:
        #         scores = [diffs_allo[k] for diffs_allo in diffs_geno 
        #                     if diffs_allo] # and (type(diffs_allo[k]) in [int, str])]
        #         if scores:
        #             result = None
        #             if isinstance(scores[0], int):
        #                 result = sum(scores)
        #             elif isinstance(scores[0], str):
        #                 result = ':'.join(scores)
        #             elif isinstance(scores[0], dict):
        #                 print(scores)
        #             if result:
        #                 diffs[k] = result
        #         # try:
        #         # except Exception as e:
        #         #     print(allele_match.__repr__(), e)    
        #         # if diffs:
        #         #     allotype_mismatches.append(allele_match)

        #         # if diffs:
        #         #     if 'score_nt' in diffs:
        #         #         score_nt += diffs['score_nt']
        #         #     if 'score_aa' in diffs:
        #         #         score_aa += diffs['score_aa']
        #         #     if 'score_nt_ard' in diffs:
        #         #         score_nt_ard += diffs['score_nt_ard']
        #         #     if 'score_aa_ard' in diffs:
        #         #         score_aa_ard += diffs['score_aa_ard']
        #     scores = diffs
        #     # self.diffs = diffs
        #     # return diffs
        # self.diffs = scores
        # return scores
        # # self.allotype_mismatches = allotype_mismatches
        # # return self.allotype_mismatches
    
    def serialize(self) -> Dict[str, str]:
        """
        Export dictionary for exposing information in the API.
        """
        output = {'genotype_recip' : self.genotype_recip.glstring,
                    'genotype_donor' : self.genotype_donor.glstring,
                    'directionality' : self.directionality,
                    # 'genotype_donor_flipped' : self.genotype_donor_flipped,
                    'grade' : self.grade
                    # 'matched_alleles_pat' : self.parse_as_str(self.matched_alleles_pat),
                    # 'matched_alleles_don' : self.parse_as_str(self.matched_alleles_don),
                    # 'mismatched_alleles_pat' : self.parse_as_str(self.mismatched_alleles_pat),
                    # 'mismatched_alleles_don' : self.parse_as_str(self.mismatched_alleles_don)
                }
        if self.diffs:
            output['diffs'] = self.diffs.serialize()
        if self.annotation:
            output['annotation'] = self.annotation
        if self.rank:
            output['rank'] = self.rank
        if self.index:
            output['index'] = self.index
        # if self.allotype_matches:
        #     output['allotype_matches'] = [match.serialize() for match in self.allotype_matches]
        return output
    
    def __repr__(self) -> str:
        return "{}-{}".format(self.genotype_recip, self.genotype_donor)