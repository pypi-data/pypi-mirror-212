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
import re
from .allotype import Allotype
from .ref_data import RefData
from typing import Union, Dict, List, Tuple
from pyard import ARD
import pandas as pd
from .dataset import Dataset

class Haplotype(object):

    def __init__(self, 
             hla : Union[str, List[Allotype], pd.core.frame.DataFrame],
             id=None, verbose : bool = False,
             ref_data : RefData = None, ard : ARD = None, sire : str = None) -> None:
        """
        Represents a pair of HLA-DPB1 alleles. Needs to be delimited by either a
        '+' (unphased) or '~' (phased) character. The order of the alleles is stored
        based on a numerical sort.

        :param typing:  Two allele names delimited by either '+' or '~' or a
            Dataframe with an 'allotype' and 'seq' column and an optional 'allotype' column.
        """
        self.verbose = verbose
        self.hla = hla
        self.id = id
        self.sire = sire
        self.ref_data = ref_data
        self.ard = ard
        self.delimiter = '^'
        self.glstring, self.allotypes = self._process_hla()
        self.annotation = {}

    def _process_hla(self) -> Tuple[str, Dict[str, Allotype]]:
        if isinstance(self.hla, list):
            allotypes = self.hla
        elif isinstance(self.hla, str):
            allotypes = self.hla.split(self.delimiter)
        else:
            raise Exception("Please input a list or string haplotype input.")
        allotypes = [Allotype(allotype, ref_data=self.ref_data, ard=self.ard, verbose=self.verbose)
                                        for allotype in allotypes]
        allotypes_new = {}
        for allotype in allotypes:
            if allotype.locus in allotypes_new:
                raise Exception('There is more than one allotype on the same locus in this haplotype.', allotypes)
            allotypes_new[allotype.locus] = allotype
        glstring = self.delimiter.join(sorted([allotype.typing for allotype in allotypes]))
        return glstring, allotypes_new

    def annotate(self) -> Dict[str, any]:
        ann = {}
        if ('DQA1' in self.allotypes) and ('DQB1' in self.allotypes):
            ann.update(self._annotate_dq_heterodimers(self.allotypes['DQA1'],
                self.allotypes['DQB1']))
        self.annotation = ann
        return self.annotation

    def _annotate_dq_heterodimers(self, dqa1_allo : Allotype, dqb1_allo : Allotype) -> Dict[str, str]:
        g1a = ['2', '3', '4', '5', '6']
        g1b = ['2', '3', '4']
        g2a = ['1']
        g2b = ['5', '6']
        group = None
        for dqa1_fam in dqa1_allo.allele_family.split('/'):
            for dqb1_fam in dqb1_allo.allele_family.split('/'):
                if (dqa1_fam in g1a) and (dqb1_fam in g1b):
                    group = 'G1'
                elif (dqa1_fam in g2a) and (dqb1_fam in g2b):
                    group = 'G2'
        # else:
        #     raise Exception('This typing does not fall into known HLA-DQ groups.')
        return {'dq_group' : group}

    def _validate_locus(self):
        """
        Validates of alleles have the same loci.
        """
        loci = set([allele.locus for allele in self.allotypes])
        if len(loci) == 1:
            return loci.pop()
        raise InvalidGenotypeError(self.glstring,
             'There is an appropriate amount of loci. Please include only one HLA locus.')
    
    def __str__(self) -> str:
        return self.glstring

    def __repr__(self) -> str:
        return self.glstring

    def serialize(self) -> Dict[str, str]:
        serialization = {'genotype' : self.name,
                'annotation' : self.annotation,
                'allotype_one' : self.allotypes[0].serialize(),
                'allotype_two' : self.allotypes[1].serialize()}
        if self.id:
            serialization['id'] = self.id
        # if self.sire:
        #     serialization['sire'] = self.sire
        return serialization
