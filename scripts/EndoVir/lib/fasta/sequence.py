#  fasta.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


from ..sequence import sequence

class FastaSequence(sequence.Sequence):

  def __init__(self, name=None, seq=None):
    super().__init__(name, seq)
    self.header = name
    self.name = name.split(' ')[0] if seq != None else seq


  def get_sequence(self):
    return ">{0}\n{1}\n".format(self.header, self.sequence)
