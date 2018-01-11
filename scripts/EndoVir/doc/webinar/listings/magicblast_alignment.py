#  magicblast_alignment.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

<<<<<<< HEAD
from . import mapping_alignment

class MagicblastAlignment(mapping_alignment.MappingAlignment):

  def __init__(self, cols):
    super().__init__(cols)
=======

class MagicblastParser:

  def __init__(self):
    self.alignments = []

  def parse(self, src):
    self.alignments = []
    for i in src:
      if i[0] != '#':
        self.alignments.append(lib.alignment.magicblast_alignment.MagicblastAlignment(i.strip().split('\t')))
>>>>>>> 424ad161050d3993fc1b71870d6d3c5eeefc0ffc
