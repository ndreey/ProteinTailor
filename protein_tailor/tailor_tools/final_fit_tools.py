import re

# Functions and classes for the final fit procedure.

def rogue_start_stops(seq,codon_type):
    """Locates the start index for start or stop codons in sequence

    Args:
        seq (str): mRNA sequence
        codon_type (str) : "start" or "stop"

    Returns:
        dict: list with positions for selected codon type
    """
    # Start and Stop codons for E_coli
    start_stop_codons = {"start": ["AUG", "GUG", "UUG"], 
                         "stop": ["UAA", "UGA", "UAG"]}
    rogues = []    
    for ss_codon in start_stop_codons[codon_type]:
        # Returns index of codon
        ss_match = re.finditer(ss_codon,seq)
        # Extends the list with the elements in the match
        rogue_ss = [match.start() for match in ss_match]
        rogues.extend(rogue_ss)
    
    return rogues


def sense_nonsense(rogues):
    """Extracts the start positions of the stop codons that are in the
    reading frame as they can cause nonsense mutations.

    Args:
        rogues (dict): Start positions of start and stop codons

    Returns:
        list: start positions of stop codons causing nonsense.
    """    
    nonsense = []
    # For each stop codon, check if it is in the reading frame
    for rogue in rogues:        
        # If in reading frame then rogue/3 = integer.
        # If frameshifted, then rogue/3 = float.
        # By using modulo, i can tell if q is a int or a float.  
        q = rogue%3
        if q == 0:
            nonsense.append(rogue)        
        # Frameshifted stop codons dont affect protein of interest.      
        else:
            pass
    print("Nonsense Mutations found: %s" % len(nonsense))
        
    return nonsense


def make_sense(seq, nonsense):
    """Removes stop codons from sequence

    Args:
        seq (str): mRNA sequence
        nonsense (list): start positions of stop codons

    Returns:
        str: sequence without nonsense mutations
    """
    
    # As nucleotides are removed, start indexes will not be true.
    # By counting the removed nt, we can compensate so start indexes
    # from nonsense holds true.    
    rmd = 0
    
    # Lets remove each codon based on the starting positions from 
    # nonsense.
    for pos in nonsense:
        # Adjusts the position based on prior removes
        # Splits sequence, removes codon and adds the seq togeter again.
        seq = seq[:pos-rmd] + seq[pos-rmd+3:]        
        rmd += 3
    
    return seq    



def shoeshine(seq, false_init):
    """Removes SD sites that could cause a false initiation by replacing
    another redundant codon.

    Args:
        seq (str): mRNA sequence
        false_init (list): list of start positions of SD sites.
    """
    # Shoeshine each position       
    for pos in false_init:
                             
        # Modulo to aquire the remainder (r)
        r = pos%3
                   
        # If integer, then not frame shifted
        # The SD start position is the first nt in codon
        # Add is how much i need to move up to get to the specific index
        # to break the SD.
        if r == 0:                        
            add = 0
            shine = "CGC" 
             
        # If r equals 1, then +1 frame shifted
        # The SD start position is in the second nt in codon     
        elif r == 1:            
            add = 1
            shine = "GAA"
            
        # If r equals 2, then +2 frame shifted
        # The SD start position is in the third nt in codon       
        elif r == 2:            
            add = 2
            shine = "GGG"   
            
        # To insert new codon to disrupt the SD
        # We split the sequence (seq u ence), change u = x and 
        # Then put it back together: seqxence
        seq = seq[:pos+add] + shine + seq[pos+add+3:]
    print("Shoe is shoeshined\n")
    return seq




def shine_dalgarno(seq):
    """Locates shine dalgarno sites across all reading frames in seq

    Args:
        seq (string): mRNA sequence

    Returns:
        list: start positions of the sd sites.
    """    
    # Finds Shine Dalgarno Site using regex.
    results = re.finditer("AGGAGG", seq)
    # One line comprehension to store start positions    
    sd_sites = [match.start() for match in results]
    
    return sd_sites



def false_initiation(sd_site, rogues):
    """Finds SD sites that are to close to start codons that are in
    risk of causing a false initiation of translation.

    Args:
        sd_site (list): list of sd sites start index
        rogues (list): positions of rogue start codons

    Returns:
        list: list of SD positions that are to close to a start codon
    """
    false_inits = []
    # Check to see if each start is 6-12 nt downstram from each sd site
    for sd in sd_site:                
        for pos in rogues:
            # If sd site is (12 or 6) nt downstream of start codon.
            if -6 >= sd-pos >= -12:
                # Add to false initiation
                false_inits.append(sd)
                # No need to continue checking this sd, so we break
                break
            else:
                pass        
            
    return false_inits




def shoeshiner(seq):
    """By utilizing collection of functions, shoeshiner will shoeshine
    (remove SHINE-DALGARNO sites) the sequence untill sequence has no
    risk of false initiations.

    Args:
        seq (str): sequence

    Returns:
        seq: sequence without false initations
    """
    dirty = True
    while dirty == True:
        # Find Start codons
        start_codons = rogue_start_stops(seq,"start")
        print("There are %s start codons" % len(start_codons))
        # Find SD sites
        sd_sites = shine_dalgarno(seq)
        print("There are %s SD-sites" % len(sd_sites))
        # Find false initiations
        false_inits = false_initiation(sd_sites, start_codons)
        print("Off those, %s are false initiations" % len(false_inits))
        
        if len(false_inits) == 0:
            print("Shoe is shiny")
            dirty = False
        else:
            print("Shoe needs shoeshine")
            seq = shoeshine(seq, false_inits)
            
    return seq



class FinalFit:
    """Final Fitting of the Tailored Protein where we check so no 
    false initations or nonsense mutations have been implemented 
    through the Codon Tailor process.
    """    
    def __init__(self, seq):
        
        try:            
            # Locate start positions of rogue stop codons
            self.rogue_stops = rogue_start_stops(seq, "stop")
            print("Stop codons: %s" % len(self.rogue_stops))
        except:
            print("ERROR@ FinalFit rogue.stops")
        
        try:
            # Start positions of stop codons that must be removed.
            self.nonsense = sense_nonsense(self.rogue_stops)            
        except:
            print("ERROR@ FinalFit nonsense")
            
        try:    
            # Remove nonsense mutations
            self.sense_seq = make_sense(seq, self.nonsense)
            print("Sequence length post make_sense: %s" % len(self.sense_seq))
        except:
            print("ERROR@ FinalFit sense_seq")        
        
        try:
            self.tailored_seq = shoeshiner(self.sense_seq)
        except:
            print("ERROR@ FinalFit tailored_seq")
