#  flank_lhs.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

from . import flank
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import extensions.extension_lhs

class LhsFlank(flank.Flank):

  def __init__(self, contig):
    super().__init__(contig, 'lhs')
    self.overlap = 5
    self.read_overlap = 20
    self.extension = extensions.extension_lhs.LhsExtension(self)

  def calculate_coordinates(self):
    self.start = 0
    self.stop = self.contig.flank_len

  def get_fasta_sequence(self):
    return ">{}\n{}\n".format(self.name, self.contig.sequence[:self.length])

  def is_extended(self, alignment):
    if alignment.read.get_ordered_coords()[1] > alignment.read.length - 20:
      if alignment.flank.get_ordered_coords()[0] == 0 and alignment.read.get_ordered_coords()[0] > 0:
        return self.extension.is_longer_alignment(alignment)
    return False
