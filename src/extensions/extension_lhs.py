#  extension_lhs.py
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>

from . import extension

class LhsExtension(extension.Extension):

  def __init__(self, flank):
    super().__init__(flank)

  def update_coordinates(self, alignment):
    self.start = self.flank.start + self.alignment.flank.get_ordered_coords()[0]
    self.stop = self.start +  self.length - 3

  def shift_coordinates(self, shift):
    self.stop += shift
