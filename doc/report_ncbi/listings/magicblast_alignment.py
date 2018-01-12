#  magicblast_alignment.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from . import mapping_alignment

class MagicblastAlignment(mapping_alignment.MappingAlignment):

  def __init__(self, cols):
    super().__init__(cols)
