import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Functions for calculating statistics and creating plots.

def GC_content(seq):
    """Returns the GC content of sequence

    Args:
        seq (str): DNA or RNA sequence

    Returns:
        int: GC content as a fraction
    """
    return round(((seq.count("C") + seq.count("G")) / len(seq)),3)



def GC_content_dist(seq,pos,name):    
    """Plots the GC content distribution in a sliding window fashion.        

    Args:
        seq (str): Sequence
        pos (int): Size of the sliding window
    """
    
    plot_gc = []
    for i in range(0, len(seq) - pos):        
        gc = [i + 1, GC_content(seq[i:i + pos])]
        plot_gc.append(gc)

    df = pd.DataFrame(plot_gc, columns = ["Pos","GC"])
    
    sns.set_style("whitegrid")
    ax = sns.relplot(df, x="Pos", y="GC", kind="line", color="red")
    ax.set(title = "%s: GC content per %s bases" % (name,pos))
    plt.savefig("temp/%s_gc.png" % name, bbox_inches='tight')
    


def caizen(freq_list):
    """Calculates the CAI of rna sequence by extracting the f(i) and
    fmax(j) from the codon frequency list

    Args:
        freq_list (list): List with codon, f(i), f(j)

    Returns:
        int: The CAI rounded to 3 decimals.
    """
    cai = 1      

    # Explain math further here!
    for f in freq_list:
        wi = f[1]/f[2]     # f(i) / fmax(j)
        cai = cai * wi

    cai = pow(cai, 1 / len(freq_list))    # product ^(1/N)
    
    return round(cai,3) 