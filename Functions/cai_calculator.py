import python_codon_tables as pct
"""
Codon Adaption Index (CAI)

CAI values range between 0 and 1. The closer to 1 the better codon optimization.
Thus, the higher, the more expressed it will be.

Formula:    w(i) = f(i) / fmax(j)           CAI = (w(i)*w(j)...w(n codons))^(1/N)   | where N is the sum of all codons - start and stop codons. 
w(i) is the relative adaptivness, you can say the weight score.
f(i) is the frequency of a codon (i) and fmax(j) is the frequency of the most often synonymous codon.

The CAI for the gene can be calculated as the product of all w(i) except start and stop codons to the power 1/sum(codons)


"""

rna = "AUGCCAGCUUUGUCUAGAUGGGCUUCUUUGCCAGGUCCAUCUAUGAGAGAAGCUGCUUUUAUGUAUUCUACUGCUGUUGCUAUUUUUUUGGUUAUUUUGGUUGCUGCUUUGCAAGGUUCUGCUCCAAGAGAAUCUCCAUUGCCAUAUCAUAUUCCAUUGGAUCCAGAAGGUUCUUUGGAA"

taxid = 168807    # E. coli O127: H6
table = pct.get_codons_table(taxid, replace_U_by_T=False)

def calc_cai(seq,table):
    """Calculates the CAI of rna sequence by extracting the f(i) and fmax(j) from the codon usage table dictionary

    Args:
        seq (str): rna sequence
        table (dictionary): Codon usage table dictionary

    Returns:
        int: Codon Adaption Index (CAI)
    """
    
    codons = []
    # Add codons to list
    # For each third nuc in sequence, append codon.
    for i in range(0,len(seq),3):    
        codons.append(seq[i:i+3])

    # For each nested list: list[0] = codon, list[1] = f(i) and list[2] = fmax(j)
    codon_freq = []

    # Unpacks table to store codon(i), freq of codon(i) and fmax(j) in codon_freq as a list.
    for codon in codons[1:]:    
        for amino in table.keys():
            # If the codon exists in this key then we extract said information to codon_freq                
            try: 
                if table[amino][codon]:
                    tmp_dict = table[amino]
                    fmax = max(tmp_dict, key = tmp_dict.get)                
                    codon_freq.append([codon, table[amino][codon], tmp_dict[fmax]])
                else:
                    pass
            except:
                pass


    # Calculate CAI
    cai = 1 
    n_codons = len(codon_freq)

    for f in codon_freq:
        wi = f[1]/f[2]     # f(i) / fmax(j)
        cai = cai * wi

    cai = pow(cai, 1 / n_codons)    # product ^(1/N)

    return round(cai,3)

print(calc_cai(rna,table))