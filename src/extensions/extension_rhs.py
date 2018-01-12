#  extension_rhs.py
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>

from . import extension

class RhsExtension(extension.Extension):

  def __init__(self, flank):
    super().__init__(flank)

  def update_coordinates(self, alignment):
    self.start = self.flank.start + alignment.flank.get_ordered_coords()[0]
    self.stop = self.start + abs(alignment.flank.stop -alignment.flank.start)

  def shift_coordinates(self, shift):
    self.start += shift
    self.stop += shift
