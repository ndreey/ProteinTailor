"""
With uniprot entry, download the aa seq
    Can handle isoforms
"""

import requests
from Bio import SeqIO
from io import StringIO


def uniprot_seq(accesion, isoform = None):
    """Access the uniprot entry fasta of uniprot accession and returns the amino acid sequence. To access the isoform of the entry, enter the specific number.
        ID: G1RL34_NOMLE, the accession is: G1RL34

    Args:
        accesion (str): The accession of the uniprot entry. 
        isoform (int, optional): Isoform number of accesion. Defaults to None.
    """
    
    # URL of the uniprot api
    up_api ="https://rest.uniprot.org/uniprotkb/search?format=fasta&includeIsoform=true&query=accession%3A" 

    # Gets the contents of the accesion id.
    response = requests.get(up_api + accesion)

    # Checks to see if we are able to access Uniprot api.
    if response.status_code != 200:
        print("error connecting to Uniprot")

    # The contents of the request in fasta format
    fasta = response.text    
    
    # If isoform of accession requested we add that specific handle to accesion.
    if isoform != None:
        record_id = accesion + "-" + str(isoform)
        
    else:
        record_id = accesion
    
    # Accesses the sequence by finding matchid record_id in fasta.    
    aa_seq = ""    
    with StringIO(fasta) as fasta_io:
        for record in SeqIO.parse(fasta_io, "fasta"):                     
            if record_id in record.id:     
                #print(record.id)
                #print(record.seq)
                aa_seq = record.seq
                break
            else:
                pass    
    
    return(aa_seq)
    

x = uniprot_seq("G1RL34")

print(x)