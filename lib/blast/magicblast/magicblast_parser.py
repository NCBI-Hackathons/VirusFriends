#  magicblast_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#  https://ncbi.github.io/magicblast/doc/output.html
#  Version: 0.0

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../...'))
import lib.alignment.magicblast_alignment

class MagicblastParser:

  def __init__(self):
    self.alignments = []

  def parse(self, src):
    self.alignments = []
    for i in src:
      if i[0] != '#':
        self.alignments.append(lib.alignment.magicblast_alignment.MagicblastAlignment(i.strip().split('\t')))
