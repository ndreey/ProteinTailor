import python_codon_tables as pct


"""
We use an already developed package for this.
CITATION TO COME. https://github.com/Edinburgh-Genome-Foundry/codon-usage-tables
"""


#Downloads the CUT for taxonid, the CUT is a dictionary.
#Key = aa, value = dictionary with codon:freq

taxid = 168807
table = pct.get_codons_table(taxid, replace_U_by_T=False)
print(table)

