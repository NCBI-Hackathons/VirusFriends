#  magicblast_alignment.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


class MappingAlignment:

  class Read:
    def __init__(self, name, start, stop, strand, qlen):

  class Flank:
    def __init__(self, name, start, stop, strand):

  def __init__(self, cols):
    self.read = self.Read(cols[0], cols[6], cols[7], cols[13], cols[15])
    self.flank = self.Flank(cols[1], cols[8], cols[9], cols[14])
    self.pident = float(cols[2])

class MagicblastParser:

  def __init__(self):
    self.alignments = []

  def parse(self, src):
    self.alignments = []
    for i in src:
      if i[0] != '#':
        self.alignments.append(MagicblastAlignment(i.strip().split('\t')))
