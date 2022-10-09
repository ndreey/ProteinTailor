"""
After manually removing the unwanted information in a txt.file i ran this to create a dictionary.
dict{aminoacid:{codon:fraction,codon2;fraction}}

The last run is for yeast.
"""

aminos = "ACDEFGHIKLMNPQRSTVWY*"
aminos = aminos.split()
dicto = {}

with open (r"C:\snooken\ProteinTailor\codontbl.txt", "r") as r:
    contents = r.read()
    c_list = contents.split()             #Split each line to an element
    
    for aa in aminos:                     
        tmp_d = {}        
        
        for i,ele in enumerate(c_list):   #Because the copy pasted information followed a pattern, i used index to create the temp dictionary.
            if ele == aa:
                tmp_d[c_list[i-4]] = c_list[i+4]
                
                dicto[aa] = tmp_d
    
print(dicto)

