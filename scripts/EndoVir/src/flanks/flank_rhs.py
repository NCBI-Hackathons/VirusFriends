#  flank_rhs.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

from . import flank
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import extensions.extension_rhs

class RhsFlank(flank.Flank):

  def __init__(self, contig):
    super().__init__(contig, 'rhs')
    self.overlap = 20
    self.read_overlap = 20
    self.extension = extensions.extension_rhs.RhsExtension(self)

  def calculate_coordinates(self):
    self.start = self.contig.length - self.contig.flank_len
    self.stop = self.contig.length

  def get_fasta_sequence(self):
    return ">{}\n{}\n".format(self.name, self.contig.sequence[-self.length:])

  def is_extended(self, alignment):
    if (alignment.flank.get_ordered_coords()[1] > (self.length - self.overlap)) and \
       (alignment.read.get_ordered_coords()[0] < self.read_overlap):
      return self.extension.is_longer_alignment(alignment)
    return False
