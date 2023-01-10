import os
import webbrowser

# Functions to build the report

def mirror_check(seq, tlrd, nonsense):
    """Creates a text file (mirror.txt) that compares the raw sequence 
    with the tailored sequence

    Args:
        seq (str): raw sequence
        tlrd (str): tailored sequence
        nonsense (list): list of start positions of stop codons causing
        nonsense mutations, that were removed.
    """
    print("Placing mirror")
    # If nonsense mutations (stop codons) were removed then the length 
    # of the sequences will differ. To make the alignment more true, 
    # lets add "***" to indicate that stop codon was removed.
    if len(nonsense) > 0:  
        add = 0             
        for pos in nonsense:            
            # We split the sequence at start pos, add *** then put 
            # sequence together.
            tlrd = tlrd[:pos+add] + "***" + tlrd[pos+add:]
            add += 3            
    else:
        print("Am i passing here?")
        pass
    
    print("Length of tlrd adjusted for make_sense: %s" % len(tlrd))
       
    # Opens file to write alignment.
    with open("temp/mirror.txt", "w") as f:        
        raw = ""          # The raw seqeunce line
        mirror = ""       # The comparision line (| means match, 
                          # empty space means missmatch)
        tailored = ""     # The tailored sequence line
        counter = 0       # To keep count of seq line length.
        
        # We want the sequence titles structured the same, thus we can 
        # call these later when we write                 
        raw_title = "raw\t\t"
        mirror_title = "\t\t"
        tailored_title = "tailored\t"              
        
        # For each nucleotide in raw sequence    
        for i, nuc in enumerate(seq):
            
            # If its the first nucleotide of the line we want its position.                        
            if counter == 0:
                raw += "%s" % str(i+1)
                tailored += "%s" % str(i+1)     
            else:
                pass       
            
            # To make it easier to read, we split the sequence so we 
            # have 10 nt then tab then 10 nt etc. So, this checks that
            # i is not the 10th nucleotide.        
            if i%10 != 0:
                counter += 1                
                raw += nuc
                tailored += tlrd[i]  
                                              
                if nuc == tlrd[i]:
                    mirror += "|"
                else:
                    mirror += " "
                    
            # As it is the 10th nucleotide we want to create a tab 
            # before continuing the seq                    
            else:
                counter += 1
                raw += "\t%s" % nuc
                tailored += "\t%s" % tlrd[i]
                                
                if nuc == tlrd[i]:
                    mirror += "\t|"
                else:
                    mirror += "\t "
            
            # We only want a sequence length of 80 each line, so when 
            # we reach 80 we write the sequence comparision. When we 
            # reach the last nucleotide we write regardless that it 
            # has not reached the 80nt length
            if counter == 70 or i == len(seq) - 1:
                
                # We add the titles, sequence and nucleotide position.
                raw_write = "%s%s\t%s\n" % (raw_title, raw, i+1)
                mirror_write = "%s%s\n" % (mirror_title, mirror)
                tailored_write = "%s%s\t%s\n" % (tailored_title, tailored, i+1)
                
                # Write to file
                f.write(raw_write)
                f.write(mirror_write)
                f.write(tailored_write)
                f.write("\n")
                
                # Reset the counter and sequence line.                
                counter = 0
                raw = ""
                mirror = ""
                tailored = ""                              
            else:
                pass  
            
            

def modify_path(folder_name, file_name):
    """
    Gets the user path to each temp and resource file and modifies it
    to counter the cascading bugs when using "\\" in the webbrowser 
    function open_new_tab() in protein_pickup().
    The chrome webbrowser was not able to aquire cwd nor handle "\\"

    Args:
        folder_name (str): name of folder
        file_name (str): name of file

    Returns:
        str: user path with forward slashes.
    """
    
    # Get the current working directory as a string
    cwd = os.getcwd()
    file_path = os.path.join(cwd, folder_name, file_name)
    modified_path = file_path.replace('\\', '/')
    return modified_path



def protein_pickup(title, raw_stats, tlrd_stats, tlrd_seq):
    """Creates the HTML Report file using a HTML template.

    Args:
        raw_stats (list): statistics of raw sequence
        tlrd_stats (list): statistics of tailored sequence
        tlrd_seq (str): the tailored sequence
    
    """        
    
    # Read the mirror check
    with open("temp/mirror.txt") as r:
        mirror = "\n" + r.read()

    # HTML string template
    html = f"""
    <html>
        <head>
            <title>ProteinTailor</title>
        </head>

        <body background={modify_path("resources", "protein_tailor_bg.png")}>
            
            <h1>
                <div style="font-family:tahoma; font-size: 26pt; font-weight: 600">ProteinTailor</div>       
                <div style="font-family:tahoma; font-size: 10pt; font-weight: 600">Job Title:   {title}</div>
            </h1>
            
            <h3 style="font-family: tahoma"> </h3>  
                
            <h3 style="font-family:tahoma">Tailored Sequence</h3>

            <textarea rows="12" cols="97" style="font-size:12pt">{tlrd_seq}</textarea>      

            <h3 style="font-family: tahoma">
            Mirror Check
            </h3>

            <textarea rows="30" cols="145" style="font-size:8pt">
                {mirror}
            </textarea>    

            <h3 style="font-family: tahoma">           
            </h3>    

            <table>        
                <tr bgcolor="lightgrey">
                    <th style="font-family: tahoma; font-size: 15pt" width="294">Statistics</th>
                    <th style="font-family: tahoma; font-size: 15pt" width="294">Raw</th>
                    <th style="font-family: tahoma; font-size: 15pt" width="294">Tailored</th>
                </tr>

                <tr bgcolor="white" align="center">
                    <td style="font-family: tahoma; font-weight: 600; font-size: 12pt">CAI</td>
                    <td style="font-family: tahoma; font-size: 12pt">{raw_stats[0]}</td>
                    <td style="font-family: tahoma; font-size: 12pt">{tlrd_stats[0]}</td>            
                </tr>

                <tr bgcolor="white" align="center">
                    <td style="font-family: tahoma; font-weight: 600; font-size: 12pt">GC</td>
                    <td style="font-family: tahoma; font-size: 12pt">{raw_stats[1]}</td>
                    <td style="font-family: tahoma; font-size: 12pt">{tlrd_stats[1]}</td>            
                </tr>

                <tr bgcolor="white" align="center">
                    <td style="font-family: tahoma; font-weight: 600; font-size: 12pt">Length</td>
                    <td style="font-family: tahoma; font-size: 12pt">{raw_stats[2]}</td>
                    <td style="font-family: tahoma; font-size: 12pt">{tlrd_stats[2]}</td>            
                </tr>
                
                <tr bgcolor="white" align="center">
                    <td style="font-family: tahoma; font-weight: 600; font-size: 12pt">Unviable Codons</td>
                    <td colspan="2" style="font-family: tahoma; font-size: 12pt">{tlrd_stats[3]}</td>
                </tr>

                <tr bgcolor="white" align="center">
                    <td style="font-family: tahoma; font-weight: 600; font-size: 12pt">Tailored Codons</td>
                    <td colspan="2" style="font-family: tahoma; font-size: 12pt">{tlrd_stats[4]}</td>
                </tr>                
                        
            </table>

            <h3 style="font-family: tahoma">GC Distribution</h3>
            <img src={modify_path("temp", "raw_gc.png")} width = '460'>
            <img src={modify_path("temp", "tailored_gc.png")} width = '460'>
        </body>
    </html>
    """

    with open("temp/ProteinTailor_Report.html", "w") as f:
        f.write(html)
    
    
    # Convert the relative file path to an absolute file path
    file_path = os.path.abspath("temp\\ProteinTailor_Report.html")
    
    webbrowser.open_new_tab(file_path)        
