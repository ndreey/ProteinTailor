"""
Transcribes cDNA to mRNA
"""

def transcribe(seq):
    """Replaces the T's with U's to make transcribe cDNA to RNA

    Args:
        seq (str): cDNA sequence
    """
    t = seq.upper()
    print(t.replace("T","U"))
    