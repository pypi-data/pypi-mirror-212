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

class MatchedFeatEnumeration(object):

    def __init__(self, 
            allotype_one : Allotype,
            allotype_two : Allotype,
            hla_class : str = None) -> None:
        self.allotype_one = allotype_one
        self.allotype_two = allotype_two
        self.hla_class = hla_class

        self.mfe_nt = self.mfe_aa = ''
        self.num_diff_nt = self.num_diff_aa = 0
        self.num_diff_nt_ard = self.num_diff_aa_ard = 0
        self.snps_nt = {}
        self.snps_aa = {}
        self._parse_data()

    def _parse_data(self) -> None:
        if (self.allotype_one == self.allotype_two):
            return None
        self.allotype_one.get_features(feats=['gene_feats'])
        self.allotype_two.get_features(feats=['gene_feats'])
        snp_dict = {}
        mfe_nt = []
        mfe_aa = []
        if (self.allotype_one.seq and self.allotype_two.seq) or (self.allotype_one.feats_searched and self.allotype_two.feats_searched):
            if not (self.allotype_one.feats_searched and self.allotype_two.feats_searched):
                self.allotype_one.parse_gene_features()
                self.allotype_two.parse_gene_features()
            if self.allotype_one.feats_searched:
                gene_feats = self.allotype_one.feats.seqs.feats.keys()
                for gene_feat in gene_feats:
                    if ((gene_feat in self.allotype_one.feats_searched.seq_features['seqs'].feats) and 
                        (gene_feat in self.allotype_two.feats_searched.seq_features['seqs'].feats)):
                            feat1 = self.allotype_one.feats_searched.seq_features['seqs'].feats[gene_feat].seq_two
                            feat2 = self.allotype_two.feats_searched.seq_features['seqs'].feats[gene_feat].seq_two

                            if feat1 != feat2:
                                loci = set([self.allotype_one.locus, self.allotype_one.locus])
                                if len(loci) != 1:
                                    raise Exception('Ensure the allotype loci are the same', loci)
                                locus = loci.pop()
                                seq_match = SeqMatch(feat1, feat2, locus=locus,
                                                    name=gene_feat)
                                snps = seq_match.snps
                                
                                mfe_nt.append(len(snps))
                                mfe_aa.append(len(set([snp.pos_outer for snp in snps if snp.missense])))

                                if snps:
                                    snp_dict[gene_feat] = snps
                            else:
                                mfe_nt.append(0)
                                mfe_aa.append(0)
                    else:
                        mfe_nt.append('*')
                        mfe_aa.append('*')
        score_nt = sum([s for s in mfe_nt if isinstance(s, int)])
        score_aa = sum([s for s in mfe_aa if isinstance(s, int)])
        mfe_nt, score_nt_ard = self.encode_mfe(mfe_nt)
        mfe_aa, score_aa_ard = self.encode_mfe(mfe_aa)
        mfe_nt = 'c.' + mfe_nt
        mfe_aa = 'p.' + mfe_aa
        self.snps = snp_dict
        num_snps_nt = {gene_feat : len(snps) for gene_feat, snps in snp_dict.items()}
        num_snps_aa = {gene_feat : len(set([snp.pos_outer for snp in snps if snp.missense])) 
                                    for gene_feat, snps in snp_dict.items()}
        num_snps_aa = {gene_feat : len_snps
            for gene_feat, len_snps in num_snps_aa.items() if len_snps}
        
        self.mfe_nt = mfe_nt
        self.mfe_aa = mfe_aa
        self.num_diff_nt = score_nt
        self.num_diff_aa = score_aa
        self.num_diff_nt_ard = score_nt_ard
        self.num_diff_aa_ard = score_aa_ard
        self.snps_nt = snp_dict
        snps_aa = {gene_feat : list(set([snp.get_aa_snp() for snp in snp_list if snp.cds])) 
            for gene_feat, snp_list in snp_dict.items()}
        snps_aa = {gene_feat : snp_list for gene_feat, snp_list in snps_aa.items() if snp_list}
        self.snps_aa = snps_aa

    def encode_mfe(self, scores : List[Snp]) -> Tuple[str, int]:
        mfe = []
        score_ard = 0
        for i, score in enumerate(scores):
            if i == 0:
                delimiter = ''
            else:
                delimiter = '_' if i % 2 == 0 else '-'
                if ((self.hla_class == '1') and ((i + 1) in [4, 6]) or 
                    (self.hla_class == '2') and ((i + 1) == 4)):
                        delimiter += 'a'
                        score_ard += score
            mfe += [delimiter, score]
        return ''.join([str(el) for el in mfe]), score_ard
        

    def serialize(self) -> Dict[str, any]:
        serialization = {'mfe_nt' : self.mfe_nt,
                    'mfe_aa' : self.mfe_aa,
                    'num_diff_nt' : self.num_diff_nt,
                    'num_diff_aa' : self.num_diff_aa,
                    'num_diff_nt_ard' : self.num_diff_nt_ard,
                    'num_diff_aa_ard' : self.num_diff_aa_ard,
                    'snps' : {feat : [str(snp) for snp in snps] for feat, snps in self.snps.items()}}
        return serialization

    def __add__(self, mfe2 : any) -> any:
        self.mfe_nt + mfe2.mfe_nt