#
# Copyright (c) 2023 Be The Match.
#
# This file is part of 
# (see https://github.com/nmdp-bioinformatics/).
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
from .ref_data import RefData
from .allotype import Allotype
from typing import List, Dict
from .annotation import Annotation

class GeneParser(object):
    
    def __init__(self, ref_data : RefData = None) -> None:
        self.n_exons = 5
        self.feature_names = self._calc_features()
        self.ref_data = ref_data or RefData()
        # self.combined_seq_locus = self._get_combined_seq_locus()

    def _calc_features(self) -> List[str]:
        """
        Calculates a list of feature names for class II loci.
        """
        feature_names = (['utr5'] + 
                         [feature + '_' + str(i)
                              for i in range(1, self.n_exons + 1) for feature in ['exon', 'intron'] 
                              if not (i == self.n_exons and feature == 'intron')] +
                         ['utr3'])
        return feature_names

    def _get_combined_seq_locus(self) -> str:
        """
        Obtains the combined seq regex for this particular locus based on all
        high-res alleles of a particular locus.
        """
        return Annotation(ref_data=self.ref_data).get_combined_seq(cds = True)

    def parse_gene_features(self, allele : str, seq : str,
                 index : int = None, id : str = None, project : str = None, method : str = None,
                source : str = None, allele_index : str = None, parsed_features : Dict[str, str] = {},
                verbose : bool = False):
        """
        Creates an Annotation object for a particular sequence.
        """
        annotation = Annotation(allele,
             seq, ref_data=self.ref_data, verbose=verbose)
        annotation.annotate()
        return annotation.parsed_features



    # def get_combined_seq(self, allele_input : Allotype) ->:
