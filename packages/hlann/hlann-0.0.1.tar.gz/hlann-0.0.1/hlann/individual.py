#
# Copyright (c) 2023 Be The Match.
#
# This file is part of Aggregate Matching Tool
# (see https://github.com/nmdp-bioinformatics/agg-match-tool).
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
from .genotype import Genotype
from .haplotype import Haplotype
from typing import List
from .ref_data import RefData
from pyard import ARD
from typing import Union, Tuple, Dict
import pandas as pd
from .dataset import Dataset

class Individual(object):
    
    def __init__(self, data : Union[str, pd.core.frame.DataFrame], id : str = None,
            ref_data : RefData = None, ard : ARD = None, verbose : bool = False) -> None:
        """
        An individual can be represented via a GL string (str) 
        or a table (pd.core.frame.DataFrame) of allotype, phase, and seq.
        """
        self.verbose = verbose
        self.data = data
        self.ref_data = ref_data
        self.loci = ['A', 'C', 'B', 'DRB1', 'DQA1', 'DQB1', 'DPB1']
        self.ard = ard
        self.id = id
        self.glstring, self.genos = self._parse_data()
        self.annotation = None
    
    def _parse_data(self) -> Tuple[str, Dict[str, Genotype]]:
        if isinstance(self.data, pd.core.frame.DataFrame):
            df = self.data.copy()
            if 'ALLOTYPE' in df:
                if 'id' in df:
                    id = set(df['id'])
                    if len(id) != 1:
                        raise Exception("You need to supply exactly one unique identifier in the 'id' column of the supplied DataFrame.")
                    self.id = id.pop()
                df.loc[:, 'LOCUS'] = df['ALLOTYPE'].str.split('*').str[0].str.replace('HLA-', '')
                df = df[df['LOCUS'].isin(self.loci)]
                df_genotypes = dict(tuple(df.groupby('LOCUS'))).values()
                genotypes = df_genotypes
            else:
                ds = Dataset(df)
                genotypes = [ds.get_dataframe(headers_locus=locus) for locus in ds.headers_locus]
                # genotypes = [ds for ds in genotypes if not ds.empty]
        elif isinstance(self.data, str):
            glstring = self.data
            genotypes = glstring.split('^')
        genotypes = [Genotype(genotype, verbose=self.verbose, ref_data=self.ref_data, ard=self.ard) for genotype in genotypes]
        glstring = '^'.join([str(genotype) for genotype in genotypes])
        # self.loci = [locus for locus in self.loci if locus in [geno.locus for geno in genotypes]]
        genotypes = {geno.locus : geno for geno in genotypes}
        return glstring, genotypes

    def annotate(self) -> Dict[str, any]:
        if self.annotation: return self.annotation
        loci = self.genos
        results = {}
        if ('DQA1' in loci) and ('DQB1' in loci):
            results.update(self._annotate_dq_heterodimers(loci))
        if 'B' in loci:
            results['b_leader'] = self._annotate_b_leader(loci['B'])
        if 'DPB1' in loci:
            results['dpb1_expr'] = self._annotate_dpb1_expr(loci['DPB1'])
            results['dpb1_tce'] = self._annotate_dpb1_tce(loci['DPB1'])
        self._annotate_pbms(loci, results)
        self.annotation = results
        return self.annotation
    
    def _annotate_pbms(self, genos : List[Genotype], results : Dict) -> None:
        for geno in genos.values():
            locus = geno.locus
            if locus in ['A', 'B', 'C']:
                geno.get_annotations(feats=['PBM'])
                results[locus + '_PBM'] = '+'.join(geno.annotation['PBM'])

    def _annotate_b_leader(self, geno : Genotype) -> str:
        geno.get_annotations(feats=['P2'])
        b_leader_geno = '+'.join([p2.replace('?', '').replace('~', '') for p2 in geno.annotation['P2']])
        return b_leader_geno
    
    def _annotate_dpb1_tce(self, geno : Genotype) -> str:
        geno.get_annotations(feats=['tce'])
        # print(geno.annotation)
        tce_geno = '+'.join([tce.replace('?', '').replace('~', '') for tce in geno.annotation['tce']])
        return tce_geno

    def _annotate_dpb1_expr(self, geno : Genotype) -> str:
        geno.get_annotations(feats=['expression'])
        expr_geno = '+'.join([expr.replace('?', '').replace('~', '')[0].upper() for expr in geno.annotation['expression']])
        return expr_geno

    def _annotate_dq_heterodimers(self, loci : Dict[str, Genotype]) -> Dict[str, any]:
        dqa1 = loci['DQA1']
        dqb1 = loci['DQB1']
        dq_molecules = {}
                # else:
                #     raise Exception('This combination is neither G1 or G2', 
                #                 (dqa1_allo.allele_family, dqb1_allo.allele_family))
        group_geno = [None, None]
        # all_hi_res = True
        split_p_groups = False
        for i, dqa1_allo in enumerate(dqa1.allotypes):
            for dqb1_allo in dqb1.allotypes:
                # if not ((len([allo.var_expression for allo in dqa1_allo.alleles_hi_res if allo.var_expression == None]) == 1) and
                #     (len([allo.var_expression for allo in dqb1_allo.alleles_hi_res if allo.var_expression == None]) == 1)):
                #         all_hi_res = False
                dqa1_p_group = dqa1_allo.p_group
                dqb1_p_group = dqb1_allo.p_group
                if ('/' in dqa1_p_group or '/' in dqb1_p_group):
                    split_p_groups = True
                    dqa1_p_group = dqa1_p_group[:-1]
                    dqb1_p_group = dqb1_p_group[:-1]

                dq_molecule = Haplotype([dqa1_p_group, dqb1_p_group],
                                    ref_data=self.ref_data, ard=self.ard)
                group = dq_molecule.annotate()['dq_group']

                # CHANGE LOGIC TO ACCOMMODATE THIS
                dqa1_allo.get_features('DQ_GROUP').serialize()['anns']['DQ_GROUP']
                dqb1_allo.get_features('DQ_GROUP').serialize()['anns']['DQ_GROUP']
                if group:
                    dqa1_allo.in_haplotype = True
                    dqb1_allo.in_haplotype = True
                    if (group_geno[i] != None) and (group_geno[i] != group):
                        raise Exception('Mismatching HLA-DQ group assignments', group_geno, group)
                    group_geno[i] = group
                    # Num DQ molecule calculation
                    # if (len(dqa1_allo.alleles_hi_res) != 1) or (len(dqb1_allo.alleles_hi_res) != 1):
                    #     raise Exception('The calculated HLA-DQ molecules are ambiguous', 
                    #         (dqa1_allo.alleles_hi_res, dqb1_allo.alleles_hi_res))
                    dq_molecule.annotation['dq_group'] = group
                    if dq_molecule.glstring not in dq_molecules:
                        dq_molecules[dq_molecule.glstring] = dq_molecule
        allos_no_dq = [allo for allo in dqa1.allotypes + dqb1.allotypes if not allo.in_haplotype] 
        if len(allos_no_dq):
            raise Exception("Not all allotypes generated HLA-DQ molecules:", allos_no_dq)
        if None in group_geno:
            raise Exception('There are not enough valid DQA1~DQB1 haplotypes in this individual.', group_geno)
        group_geno = '+'.join(group_geno) if not len(allos_no_dq) else None
        num_dqs = len(dq_molecules) if not split_p_groups else None
        dq_heterodimers = list(dq_molecules.values()) if not split_p_groups else None
        result = {'num_dqs' : num_dqs,
                  'dq_groups' : group_geno,
                  'dq_heterodimers' : dq_heterodimers}
        return result

    def serialize(self) -> Dict[str, any]:
        output = {'glstring' : self.glstring}
        output['genotypes'] = {locus : geno.serialize() for locus, geno in self.genos.items()}
        if self.annotation:
            output['annotation'] = self.annotation
            if 'dq_heterodimers' in output['annotation']:
                if output['annotation']['dq_heterodimers']:
                    output['annotation']['dq_heterodimers'] = [str(haplo) for haplo in output['annotation']['dq_heterodimers']]
        return output

    def __repr__(self):
        return self.glstring