import requests
from Bio import SeqIO
from io import StringIO

# Functions to handle inputs

def strip_input(user_input):
    """Stores ID and SEQ if fasta format. 
    Otherwise just strips input of leading or trailing whitespaces.

    Args:
        user_input (str): user input

    Returns:
        list: [id, seq]
    """
    # If fasta format, store ID and SEQ using SeqIO    
    if user_input.find(">") == 0:                
        try:                      
            with StringIO(user_input) as fasta_io:                
                for record in SeqIO.parse(fasta_io, "fasta"):                  
                    user_input = record.seq
        except:            
            print("ERROR@strip_input()")
            print("> was found but input not in fasta format?")  
    
    # If not, we clean up input making it UPPER and removing whitespace.                  
    else:
        user_input = user_input.upper()
        user_input = user_input.rstrip()
        user_input = user_input.replace("\n", "")       
    
    return user_input



def taxid_check(input_taxids):
    """Checks that taxids enterd are digits

    Args:
        input_taxids (list): [organism_taxid, host_taxid]

    Returns:
        list: [organism_taxid, host_taxid]
    """
    taxids = []        
    for taxid in input_taxids:
        # Removes whitespaces        
        taxid = taxid.rstrip()
        # If string consists of digits
        if taxid.isdigit():
            taxids.append(taxid)
        else:
            print("ERROR@ taxid_check()")
            print("User did not enter digits")
    # Return user input if botht taxids are clean            
    if len(taxids) == 2:
        return taxids
    else:
        pass



def uniprot_seq(accesion, isoform = None):
    """Access the uniprot entry fasta of uniprot accession and returns
    the amino acid sequence. To access the isoform of the entry, enter 
    the specific number. ID: G1RL34_NOMLE, the accession is: G1RL34

    Args:
        accesion (str): The accession of the uniprot entry. 
        isoform (int, optional): Isoform number of accesion.
        Defaults to None.
    """
    
    # URL of the uniprot api
    up_api = "https://rest.uniprot.org/uniprotkb/search?format=fasta& \
        includeIsoform=true&query=accession%3A" 

    # Gets the contents of the accesion id.
    response = requests.get(up_api + accesion)

    # Checks to see if we are able to access Uniprot api.
    if response.status_code != 200:
        print("ERROR@ uniprot_seq()")
        print("We did not recieve the 200 status code, try again, \
            uniprot could be down")

    # The contents of the request in fasta format
    fasta = response.text    
    
    # If isoform of accession requested we add that specific handle 
    # to accesion.
    if isoform != None:
        record_id = accesion + "-" + str(isoform)
        
    else:
        record_id = accesion
    
    # Accesses the sequence by finding matchid record_id in fasta.
    # WE break after first sequence as the fasta string can hold 
    # multiple isoforms.    
    aa_seq = ""    
    with StringIO(fasta) as fasta_io:
        for record in SeqIO.parse(fasta_io, "fasta"):                     
            if record_id in record.id:
                aa_seq = record.seq
                break
            else:
                pass    
    
    return aa_seq