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
from .individual import Individual
from typing import List, Dict
from .ref_data import RefData
from .genotype_match import GenotypeMatch
from .allotype_match import AllotypeMatch
from .haplotype_match import HaplotypeMatch
from pyard import ARD
import pandas as pd
from typing import Tuple, Union
from .dataset import Dataset
from .util import flatten_dict

class IndividualMatch(object):
    
    def __init__(self, data : Union[List[str], pd.core.frame.DataFrame] = None,
                recip : str = None,
                donor : str = None,
                ref_data : RefData = None,
                loci : List[str] = ['A', 'C', 'B', 'DRB1', 'DQA1', 'DQB1', 'DPB1'],
                 ard : ARD = None, verbose : bool = False) -> None:
        """
        individual_one/two: Either glstring or id label for a supplied table.
        table: A table with rows of allotypes and sequences for two individuals.
            Used for sequence-based matching.
            Consists of these headers: id, allotype, seq.
        """
        self.data = data
        self.ref_data = ref_data
        self.ard = ard
        self.loci = loci
        self.verbose = verbose
        self.recip = recip
        self.donor = donor
        self.matches = []
        self.glstrings, self.individuals = self._parse_data()
        self.recip, self.donor = self.individuals
        self.geno_matches = []
        self.allotype_mismatches = {}
        self.annotation = {}
        #  = self._parse_glstring()
    
    def _parse_data(self) -> Tuple[List[str], List[Individual]]:
        seqs =  None
        glstrings = None
        data = self.data
        if isinstance(data, pd.core.series.Series):
            data = data.to_frame().transpose()
        if isinstance(data, list) and len(data) and isinstance(data[0], dict):
            data = pd.DataFrame(data)
        if isinstance(data, pd.core.frame.DataFrame):
            df = data.copy()
            ds = Dataset(df)
            if 'ALLOTYPE' in ds.df:
                df.columns = [col.upper() for col in df.columns]
                df['LOCUS'] = df['ALLOTYPE'].str.split('*').str[0].str.replace('HLA-', '')
                df = df[df['LOCUS'].isin(self.loci)]
                df_individuals = dict(tuple(df.groupby('ID'))).values()
                if len(df_individuals) != 2:
                    raise Exception("There needs to be exactly two non-unique IDs in the column.", df['id'])
                individuals = df_individuals
            else:
                subjs = ds.headers['subjects']
                if len(subjs) != 2:
                    raise Exception("There needs to be exactly two subjects detected in this dataframe.", subjs)
                individuals = [ds.get_dataframe(headers_subj=subj) for subj in subjs]
        elif isinstance(data, list):
            if (len(data) == 2):
                individuals = data
            else:
                raise Exception("The supplied list needs to contain two GL strings.")
        elif self.recip and self.donor:
            glstrings = [self.recip, self.donor]
            individuals = glstrings
        else:
            raise Exception("The data supplied needs to either be a Pandas DataFrame or a list.")
        individuals = [Individual(individual, ref_data=self.ref_data, ard=self.ard, verbose=self.verbose)
            for individual in individuals]
        glstrings = sorted([individual.glstring for individual in individuals])
        self.loci = list(set([locus for individual in individuals for locus in individual.genos.keys()]))
        return glstrings, individuals

    # def _parse_glstrings(self) -> List[Individual]:
    #     individuals = []
    #     for glstring in self.glstrings:
    #         individuals.append(Individual(glstring, ref_data=self.ref_data, ard=self.ard))
    #     return individuals

    def calc_matches(self, align_mismatches_only : bool = True) -> Tuple[List[GenotypeMatch], Dict[str, str]]:
        # SLUG : Single-locus unambiguous genotype
        geno_matches = {}
        for individual in self.individuals:
            for slug in individual.genos.values():
                if slug.locus not in geno_matches:
                    geno_matches[slug.locus] = []
                geno_matches[slug.locus].append(slug)
        results = {}
        allotype_mismatches_total = []
        annotation = {}
        for geno_match in geno_matches.values():
            if len(geno_match) == 2:
                geno_match = GenotypeMatch(geno_match[0], geno_match[1])
                # allotype_mismatches = 
                if all([allo.seq for geno in geno_match.genotypes for allo in geno.allotypes]):
                    geno_match.get_genotype_diffs(align_mismatches_only=align_mismatches_only)
                annotation.update(geno_match.annotate())
                if geno_match.locus in results:
                    raise Exception('Locus already in results', results)
                results[geno_match.locus] = geno_match
                # if allotype_mismatches:
                #     if self.verbose:
                #         print(allotype_mismatches)
                # allotype_mismatches_total += allotype_mismatches
        self.geno_matches = results
        # allotype_mismatches = {locus : [] for locus in self.loci}
        # for allotype_mm in allotype_mismatches_total:
        #     allotype_mismatches[allotype_mm.locus].append(allotype_mm)
        # self.allotype_mismatches = allotype_mismatches
        return self.geno_matches, annotation #self.allotype_mismatches

    def _calc_hla_scoring(self) -> Dict[str, int]:
        scores = {8 : ['A', 'B', 'C', 'DRB1'],
                10 : ['A', 'B', 'C', 'DRB1', 'DQB1'],
                12 : ['A', 'B', 'C', 'DRB1', 'DQB1', 'DPB1']}
        results = {}
        for n, loci in scores.items():
            numhires = 0
            for locus, geno_match in self.geno_matches.items():
                if locus in loci:
                    numhires += geno_match.grade.count('P') + geno_match.grade.count('A')
            results['numhires' + str(n)] = numhires
        
        return results

    def _calc_dq_heterodimer_mismatching(self) -> Tuple[int, List[str]]:
        dqs_pat = self.individuals[0].annotate()
        dqs_don = self.individuals[1].annotate()
        if (not ('dq_heterodimers' in dqs_pat and 'dq_heterodimers' in dqs_don and
            dqs_pat['dq_heterodimers'] and dqs_don['dq_heterodimers'])):
                # self.matches += []    
                return None, None
        dqs_pat = dqs_pat['dq_heterodimers'].copy()
        dqs_don = dqs_don['dq_heterodimers'].copy()
        dqs_don_full = dqs_don.copy()
        haplo_matches = []
        dq_group_mismatches = []
        for dq_pat in dqs_pat:
            matched = False
            if not len(dqs_don):
                dqs_don = dqs_don_full
            for dq_don in dqs_don:
                # if not ((len([allo.var_expression for allo in dq_pat.alleles_hi_res if allo.var_expression == None]) == 1) and
                #     (len([allo.var_expression for allo in dq_don.alleles_hi_res if allo.var_expression == None]) == 1)):
                #         raise Exception('We need high resolution for both DQA1 and DQB1 typing.')
                haplo_match = HaplotypeMatch(dq_pat, dq_don)
                if haplo_match.matched:
                    dqs_don.remove(dq_don)
                    haplo_matches.append(haplo_match)
                    matched = True
                    break
            # print(dq_pat, dq_don, matched)
            if not matched:
                if dqs_don:
                    dq_don_last = dqs_don.pop(0)
                dq_group_mismatches.append(dq_pat.annotation['dq_group'])
                haplo_matches.append(HaplotypeMatch(dq_pat, dq_don_last))
        self.matches += haplo_matches
        return len([match for match in haplo_matches if not match.matched]), dq_group_mismatches

    def annotate(self, align_mismatches_only : bool = True) -> Dict[str, any]:
        annotation = {}
        geno_matches, geno_ann = self.calc_matches(align_mismatches_only=align_mismatches_only)
        annotation.update(geno_ann)
        annotation.update(self._calc_hla_scoring())
        if ('DQA1' in self.loci) and ('DQB1' in self.loci):
            num_dq_mismatches, dq_group_mismatch = self._calc_dq_heterodimer_mismatching()
            if num_dq_mismatches != None:
                annotation['num_dq_mismatches'] = num_dq_mismatches
                annotation['dq_group_mismatch'] = dq_group_mismatch
        self.annotation = annotation
        return annotation

    def serialize(self) -> Dict[str, any]:
        output = {'glstrings' : self.glstrings}
        output['recip'] = self.recip.serialize()
        output['donor'] = self.donor.serialize()
        if self.annotation:
            output['annotation'] = self.annotation
        if self.matches:
            output['matches'] = [str(match) for match in self.matches]
        output['geno_matches'] = {locus : geno_match.serialize() for locus, geno_match in self.geno_matches.items()}
        if self.allotype_mismatches:
            output['allotype_mismatches'] = {locus : [match.serialize() for match in matches]
                         for locus, matches in self.allotype_mismatches.items()}
        return output

    def to_dataframe(self, mode : str = 'horizontal') -> pd.core.frame.DataFrame:
        serialization = self.serialize()
        results = serialization #['geno_matches']
        if mode == 'horizontal':
            exceptions = []
        elif mode == 'vertical':
            exceptions = self.loci
            results = results['geno_matches']
        results = flatten_dict(results, exceptions=exceptions)
        if mode == 'vertical':
            results = {k.upper() : result for k, result in results.items()}
            results = pd.DataFrame(results.values(), index=results.keys())
            # results.columns = [col.upper() for col in results.columns]
        else:
            results.update(serialization['annotation'])
            results = {k.upper() : [result] for k, result in results.items()}
            results = pd.DataFrame(results)
        return results

    def __repr__(self):
        return ' '.join(self.glstrings)