import python_codon_tables as pct
from tailor_tools.codon_tailor_tools import *
from tailor_tools.final_fit_tools import *
from tailor_tools.input_tools import *
from tailor_tools.report_tools import *
from tailor_tools.sequence_tools import *
from tailor_tools.statistics_tools import *

# Class that orchestrates the tailoring steps.

class ProteinTailor():
    """
    The `ProteinTailor` class provides a tool for codon optimization of 
    a given mRNA or cDNA sequence for a specified host organism. 
    It handles user inputs, gets the codon usage tables (CUTs), then 
    optimizes the sequence and provide statistics of the optimization.
    The class then outputs the tailored sequences with additional 
    information in a HTML report file.
    """
    def __init__(self, input_type, user_input, org_taxid, host_taxid, 
                 job_title):
        """
        Initialize the ProteinTailor class with parameters

        Args:
            input_type (str): type of input, options are 'cDNA', 'mRNA',
            'aa-seq', 'Uniprot'
            user_input (str): The user input, the sequence for 
            processing
            org_taxid (int): Taxonomy id of the organism the sequence 
            originates from
            host_taxid (int): Taxonomy id of the host organism the 
            sequence is going to be expressed in
            job_title (str): Title for the job
        """
        
        # Cleans up input.        
        print("\nProteinTailor STARTED")
        print("Job Title: %s" % job_title)
        print("Processing inputs...")       
        input_info = strip_input(user_input)
        print("...")
        taxids = taxid_check([org_taxid, host_taxid])
        print("...")        
        
        
        
        self.input = input_info       
        self.type = input_type        
        self.o_id = int(taxids[0])
        self.h_id = int(taxids[1]) 
        self.title = job_title.rstrip()   
        
        # Gets the Codon Usage Tables
        org_cut = pct.get_codons_table(self.o_id, replace_U_by_T=False)
        host_cut = pct.get_codons_table(self.h_id, replace_U_by_T=False)
        print("CUTs are aquired")        
        
        # How to handle input format
        try:            
            if input_type == "cDNA":                       
                seq = transcribe(self.input)            
                pass
            
            elif input_type == "mRNA":
                seq = self.input
                pass
            
            elif input_type == "aa-seq":
                seq = reverse_translate(self.input, org_cut)
                pass
            
            elif input_type == "Uniprot":
                aa_seq = uniprot_seq(self.input)
                seq = reverse_translate(aa_seq, org_cut)
                pass
                        
            else:
                pass
        except:
            print("Error@ Handeling Input Format")            
        
        # Storing the sequence
        self.seq = seq
        print("%s was converted to mRNA" % input_type)        
        print("Length of seq: %s" % len(self.seq))
        
        # Codon optimize, (Codon Tailor (CT))        
        print("\nCodonTailor initiated...")        
        ct = CodonTailor(self.seq, org_cut, host_cut)        
        print("CodonTailor succeeded")     
                   
        # Stats
        raw_cai = ct.raw_cai
        raw_gc = GC_content(self.seq)
        raw_len = len(self.seq)
        raw_stats = [raw_cai, raw_gc, raw_len]
        print("Raw Statistics: %s" % raw_stats)

        # Final Fitting
        print("\nFinalFit initiated...")
        ff = FinalFit(ct.ct_seq)        
        print("FinalFit succeeded")
                
        # Stats and important variables for Tailored Sequence
        tailored_codons = list_codons(ff.tailored_seq)
        tailored_codons_frq = codon_optimize(tailored_codons, org_cut, 
                                             host_cut)
        tailored_cai = caizen(tailored_codons_frq[3])
        tailored_gc = GC_content(ff.tailored_seq)
        tailored_len = len(ff.tailored_seq)
        unviable_codons = ct.na_codons
        tailored_codons = ct.tailored
        tailored_stats = [tailored_cai, tailored_gc, tailored_len, 
                          unviable_codons, tailored_codons]
        print("Tailored Statistics: %s" % tailored_stats)               
        
        # Reverse transcribe to DNA
        self.raw_dna = reverse_transcribe(self.seq)
        self.tailored_dna = reverse_transcribe(ff.tailored_seq)
        print("\nmRNA seq is converted to DNA")
        
        # Creates the seqeuence alignment comparision
        mirror_check(self.raw_dna, self.tailored_dna, ff.nonsense)
        print("\nMirror is in place")
        
        # Creates the GC distribution graphs        
        GC_content_dist(self.raw_dna, 80, "raw")
        GC_content_dist(self.tailored_dna, 80, "tailored")
        print("Plots are drawn")
        
        # HTML output
        protein_pickup(self.title, raw_stats, tailored_stats, 
                       self.tailored_dna)
        print("\nThe Tailored Protein is ready for pickup!")
