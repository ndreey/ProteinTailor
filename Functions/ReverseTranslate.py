import python_codon_tables as pct

def revTranslate(seq,table):
    """Reverse translates amino acid sequence to rna sequence using codon usage table

    Args:
        seq (string): amino acid sequence
        table (dictionary): codon usage table

    Returns:
        string: reverse translated rna sequence
    """
    
    seq = seq.upper()
    rna = ""
    for amino in seq:
        aaDict = table[amino]
        codon = max(aaDict, key = aaDict.get)
        rna = rna + codon
    return rna

aa = "MPALSRWASLPGPSMREAAFMYSTAVAIFLVILVAALQGSAPRESPLPYHIPLDPEGSLE"

#Downloads the CUT for e.coli, the CUT is a dictionary.
#Key = aa, value = dictionary with codon:freq
table = pct.get_codons_table("e_coli_316407", replace_U_by_T=False)

print(revTranslate(aa,table))


"""
Some info regarding pct:
Checks available tables.
print("Available tables:", pct.available_codon_tables_names)

"""



