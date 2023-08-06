#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) University of St Andrews 2022
# (c) University of Strathclyde 2022
# (c) James Hutton Institute 2022
# Author:
# Emma E. M. Hobbs

# Contact
# eemh1@st-andrews.ac.uk

# Emma E. M. Hobbs,
# Biomolecular Sciences Building,
# University of St Andrews,
# North Haugh Campus,
# St Andrews,
# KY16 9ST
# Scotland,
# UK

# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Explore the intracellular (I) and extracellular (E) CAZymes"""


import pandas as pd

from tqdm import tqdm


def get_ie_fams(fgp_df):
    """Identify families with intracellular, extracellular or both intra- and extra-cellular CAZymes
    
    :param fgp_df: df containing fams, taxs and genomes
    
    Return (return fam annotations exclude i_ and e_ prefix)
    * intra_fams: set of all fams with intracellular CAZymes
    * extra_fams: set of all fams with extracellular CAZYmes
    * intra_only_fams: set of fams with only I CAZymes
    * extra_only_fams: set of fams with only E CAZymes
    * both_intra_extra_fams: set of fams with both I and E CAZymes
    * all_fams: set of all fams
    """
    # separate fams into those with I and E CAZymes
    intra_fams = set()
    extra_fams = set()

    for ri in tqdm(range(len(fgp_df)), desc="Identifying IE fams"):
        fam = fgp_df.iloc[ri]['Fam']
        if fam.startswith('i'):
            intra_fams.add(fam.split("_")[-1])
        else:
            extra_fams.add(fam.split("_")[-1])
    print(
        f"Num of fams with intracellular CAZymes: {len(intra_fams)}\n"
        f"Num of fams with extracellular CAZymes: {len(extra_fams)}"
    )
    
    # split fams into only intracellular, only extracellular, and both 
    intra_only_fams = set()
    extra_only_fams = set()
    both_intra_extra_fams = set()
    all_fams = set([fam.split("_")[-1] for fam in fgp_df['Fam']])

    for fam in tqdm(all_fams,desc="identifying IE fams"):
        if (fam in intra_fams) and (fam in extra_fams):
            both_intra_extra_fams.add(fam)

        elif (fam in intra_fams) and (fam not in extra_fams):
            intra_only_fams.add(fam)

        elif (fam not in intra_fams) and (fam in extra_fams):
            extra_only_fams.add(fam)

        else:
            print(f"Could not find IE classification for {fam}")

    print(
        f"Total fams: {len(all_fams)}\n"
        f"Num of fams with intracellular ONLY CAZymes: {len(intra_only_fams)}\n"
        f"Num of fams with extracellular ONLY CAZymes: {len(extra_only_fams)}\n"
        f"Num of fams with BOTH intracellular and extracellular CAZymes: {len(both_intra_extra_fams)}"
    )   
    
    return intra_fams, extra_fams, intra_only_fams, extra_only_fams, both_intra_extra_fams, all_fams
