from tailor_tools.statistics_tools import caizen
from tailor_tools.sequence_tools import list_codons

# Functions and classes for codon optimization.

def codon_optimize(codons,org_cut, host_cut):
    """Codon Optimizes the sequence by choosing the most frequent codon 
    from the host CUT. If the organism codon does not exist in the host
    CUT, it then checks which aa that codon coded for and maps the aa 
    to the host CUT and picks most frequent codon.

    Args:
        codons (list): ordered list of codons
        host_cut (dict): host codon usage table dictionary
        org_cut (dict): organism codon usage table dictionary

    Returns:
        list: List with optimised sequence, number of codons that did 
        not exist in host, number of codons optimised and list of lists 
        holding each codons f(i) and f(j). 
    """
    optimized_seq = ""       # Codon Optimised sequence
    na_codons = 0            # Number of codons not existing in host CUT    
    tailored = 0             # Number of codons tailored
    codon_freq = []          # List holding [codon,f(i), f(j)]
    
    for codon in codons:                   
        for amino in host_cut.keys():
            
            # If the codon exists in the host CUT, we extract the codon 
            # with highest freq.                    
            try:                                   
                if host_cut[amino][codon]:                            
                    tmp_dict = host_cut[amino]
                    
                    # Aquires the codon with the highest freq
                    fmax = max(tmp_dict, key = tmp_dict.get)
                    
                    # [codon, f(i), f(j)] gets appended to codon_freq
                    codon_freq.append([codon, host_cut[amino][codon],
                                       tmp_dict[fmax]])
                    
                    # tailored is increased as codon was not equal to
                    # the fmax, meaning that we optimised it.
                    if codon != fmax:
                        tailored += 1
                        
                    # Rebuilding the sequence with fmax codon.                                                
                    optimized_seq = optimized_seq + fmax
                    
                    # Break, so we start over from first amino.                            
                    break
                 
                # If the codon did not exist, we aquire the amino acid 
                # it translates for.
                else:                   
                    na_codons += 1                                                
                    for amino in org_cut.keys():                        
                        # With the amino acid, we extract the codon 
                        # with max freq from h_cut.
                        try: 
                            if org_cut[amino][codon]:
                                tmp_dict = host_cut[amino]
                                fmax = max(tmp_dict, key = tmp_dict.get)
                                codon_freq.append([codon, 0.1,
                                                   tmp_dict[fmax]])
                                optimized_seq = optimized_seq + fmax
                                tailored += 1
                                break
                        except:
                            pass                           
                    break
            except:
                pass                 
    return [optimized_seq, na_codons, tailored, codon_freq] 



class CodonTailor:   
        
    def __init__(self, seq, org_cut, host_cut):
        """Utilizing a collection of functions CodonTailor codon 
        optimizes the sequence and aquires statistics.

        Args:
            seq (str): raw sequence
            org_cut (dict): organism codon usage table dictionary
            host_cut (dict): host codon usage table dictionary
        Return:
            self.raw_cai: Codon Adaption Index of pre optimised sequence
            self.ct_seq: Codon optimised sequence
            self.na_codons: Number codons that host can't handle
            self.tailored: Number of codons optimized
        """
        # Splits string into codons.
        codons = list_codons(seq)
        
        # If the sequence is comprised of only codons we continue.
        if len(codons)*3 == len(seq):            
            results = codon_optimize(codons, org_cut, host_cut)           
            raw_cai = caizen(results[3])            
        
        self.raw_cai = raw_cai       
        self.ct_seq = results[0]       # Codon optimised sequence
        self.na_codons = results[1]    # number n/a codons
        self.tailored = results[2]     # number of codons optimised 