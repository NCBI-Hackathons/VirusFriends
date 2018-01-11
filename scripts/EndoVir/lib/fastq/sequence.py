#  fastq.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from .. import sequence

class FastqSequence(sequence.sequence.Sequence):

  def __init__(self, name, seq, qual=''):
    super().__init__(name, seq)
    self.quality = qual

  def subseq(self, start, length, name=None):
    if name == None:
      return FastqSequence(self.name, self.sequence[start:start+length], self.quality[start:start+length])
    return FastqSequence(name, self.sequence[start:start+length], self.quality[start:start+length])

  def get_sequence(self):
    return "@{0}\n{1}\n+\n{2}\n".format(self.name, self.sequence, self.quality)
