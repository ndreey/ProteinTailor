# Functions for central dogma functions and sequence manipulation

def transcribe(seq):
    """Replaces the T's with U's to transcribe cDNA to RNA

    Args:
        seq (str): cDNA sequence
    """
    seq = seq.upper()
    return seq.replace("T","U")



def reverse_transcribe(seq):
    """Replaces the T's with U's to transcribe cDNA to RNA

    Args:
        seq (str): cDNA sequence
    """
    seq = seq.upper()
    return seq.replace("U","T")



def reverse_translate(seq,cut):
    """Reverse translates amino acid sequence to rna sequence using
    codon usage table. To access standard codon usage tables one can
    set cut = 1 or 2.

    Args:
        seq (str): amino acid sequence
        table (dict): codon usage table or 1 = standard e_coli, 
        2 = standard yeast

    Returns:
        str: reverse translated rna sequence
    """
    # Standard CUT table for e_coli and yeast
    e_coli = {
        'A': {'GCU': '0.18', 'GCC': '0.26', 'GCA': '0.23', 'GCG': '0.33'},
        'C': {'UGU': '0.46', 'UGC': '0.54'},
        'D': {'GAU': '0.63', 'GAC': '0.37'},
        'E': {'GAA': '0.68', 'GAG': '0.32'},
        'F': {'UUU': '0.58', 'UUC': '0.42'},
        'G': {'GGU': '0.35', 'GGC': '0.37', 'GGA': '0.13', 'GGG': '0.15'},
        'H': {'CAU': '0.57', 'CAC': '0.43'},
        'I': {'AUU': '0.49', 'AUC': '0.39', 'AUA': '0.11'}, 
        'K': {'AAA': '0.74', 'AAG': '0.26'}, 
        'L': {'UUA': '0.14', 'UUG': '0.13', 'CUU': '0.12', 'CUC': '0.10', 
              'CUA': '0.04', 'CUG': '0.47'},
        'M': {'AUG': '1.00'},
        'N': {'AAU': '0.49', 'AAC': '0.51'},
        'P': {'CCU': '0.18', 'CCC': '0.13', 'CCA': '0.20', 'CCG': '0.49'}, 
        'Q': {'CAA': '0.34', 'CAG': '0.66'}, 
        'R': {'CGU': '0.36', 'CGC': '0.36', 'CGA': '0.07', 'CGG': '0.11', 
              'AGA': '0.07', 'AGG': '0.04'}, 
        'S': {'UCU': '0.17', 'UCC': '0.15', 'UCA': '0.14', 'UCG': '0.14', 
              'AGU': '0.16', 'AGC': '0.25'}, 
        'T': {'ACU': '0.19', 'ACC': '0.40', 'ACA': '0.17', 'ACG': '0.25'}, 
        'V': {'GUU': '0.28', 'GUC': '0.20', 'GUA': '0.17', 'GUG': '0.35'}, 
        'W': {'UGG': '1.00'}, 
        'Y': {'UAU': '0.59', 'UAC': '0.41'}, 
        '*': {'UAA': '0.61', 'UAG': '0.09', 'UGA': '0.30'}}    
    
    yeast = {
    'A': {'GCU': '0.38', 'GCC': '0.22', 'GCA': '0.29', 'GCG': '0.11'}, 
    'C': {'UGU': '0.63', 'UGC': '0.37'}, 
    'D': {'GAU': '0.65', 'GAC': '0.35'}, 
    'E': {'GAA': '0.71', 'GAG': '0.29'}, 
    'F': {'UUU': '0.59', 'UUC': '0.41'}, 
    'G': {'GGU': '0.47', 'GGC': '0.19', 'GGA': '0.22', 'GGG': '0.12'}, 
    'H': {'CAU': '0.64', 'CAC': '0.36'}, 
    'I': {'AUU': '0.46', 'AUC': '0.26', 'AUA': '0.27'}, 
    'K': {'AAA': '0.58', 'AAG': '0.42'}, 
    'L': {'UUA': '0.28', 'UUG': '0.29', 'CUU': '0.13', 'CUC': '0.06', 
          'CUA': '0.14', 'CUG': '0.11'}, 
    'M': {'AUG': '1.00'}, 
    'N': {'AAU': '0.59', 'AAC': '0.41'}, 
    'P': {'CCU': '0.31', 'CCC': '0.15', 'CCA': '0.41', 'CCG': '0.12'}, 
    'Q': {'CAA': '0.69', 'CAG': '0.31'}, 
    'R': {'CGU': '0.15', 'CGC': '0.06', 'CGA': '0.07', 'CGG': '0.04', 
          'AGA': '0.48', 'AGG': '0.21'}, 
    'S': {'UCU': '0.26', 'UCC': '0.16', 'UCA': '0.21', 'UCG': '0.10', 
          'AGU': '0.16', 'AGC': '0.11'}, 
    'T': {'ACU': '0.35', 'ACC': '0.22', 'ACA': '0.30', 'ACG': '0.13'}, 
    'V': {'GUU': '0.39', 'GUC': '0.21', 'GUA': '0.21', 'GUG': '0.19'}, 
    'W': {'UGG': '1.00'}, 
    'Y': {'UAU': '0.56', 'UAC': '0.44'}, 
    '*': {'UAA': '0.48', 'UAG': '0.24', 'UGA': '0.29'}}    
    
    # Checks which standard CUT to use if wanted.
    if cut == 1:
        table = e_coli    
    elif cut == 2:
        table = yeast    
    else: 
        table = cut
        
    seq = seq.upper()
    rna = ""
    # Gets the codon with highest frequency and adds it to the string.
    for amino in seq:
        aa_dict = table[amino]
        codon = max(aa_dict, key = aa_dict.get)
        rna = rna + codon
    
    return rna



def list_codons(seq):
    """Subsets the string into an ordered list of codons.

    Args:
        seq (str): mRNA sequence

    Returns:
        list: Ordered list of codons
    """
    
    # For each third nuc in sequence, we substring that nuc and the two
    # following nucs to the list.   
    codons = [seq[i:i+3] for i in range(0,len(seq),3)]
    
    return codons
