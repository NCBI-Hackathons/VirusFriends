#  sequence.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

class Sequence:

  def __init__(self, name=None, seq=None):
    self.name = name
    self.sequence = seq
    self.length = 0 if seq == None else len(seq)
    self.dna_comp_tbl =  str.maketrans("ACTG", "TGAC")

  def subseq(self, start, length, name=None):
    return self.sequence[start:start+length]

  def revcomp(self, beg=0, end=0):
    if end == 0:
      end = self.length
    revcomp_seq = self.sequence.translate(self.dna_comp_tbl)
    revcomp_seq = revcomp_seq[end:beg]
    return Sequence(name="{}_revcomp".format(self.name),
                    seq=revcomp_seq)
