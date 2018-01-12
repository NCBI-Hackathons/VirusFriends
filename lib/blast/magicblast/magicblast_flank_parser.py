#  magicblast_flank_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../'))
from . import magicblast_parser
from lib.alignment import magicblast_alignment

class MagicblastFlankParser(magicblast_parser.MagicblastParser):

  def __init__(self, flankmap):
    super().__init__()
    self.flankmap = flankmap
    self.extensions = {}

  """
    This is a  weak test considering partial mappings onto the flank
  """
  def check_single_extension(self, flank, alignment):
    if alignment.read.get_ordered_coords()[0] < 1:
      if is_extended(alignment):
        self.extensions[flank.name] = alignment
        #print("{}: LHS Overlap {} :: Len: {}".format(flank.name,
                                                     #flank.overlap.rowid,
                                                     #flank.overlap.length))
    if alignment.read.get_ordered_coords()[1] < alignment.read.length:
      if is_extended(alignment):
        self.extensions[flank.name] = alignment
        #print("{}: RHS Overlap {} :: Len: {}".format(flank.name,
                                                     #flank.overlap.rowid,
                                                     #flank.overlap.length))

  def identify_overlaps(self, cols, flank):
    a = magicblast_alignment.MagicblastAlignment(cols)
    #print("Aligned:", a.ref.name, a.qry.name, a.qry.aln_length, a.qry.aln_length, flank.contig.hasRhsFlank)
    #print("Qry\t{}\t{}\t{}\t{}".format(a.qry.start, a.qry.stop, a.qry.strand, a.qry.length))
    #print("Ref\t{}\t{}\t{}".format(a.ref.start, a.ref.stop, a.ref.strand))
    if not flank.contig.hasRhsFlank:
      if flank.name not in self.extensions:
        self.extensions[flank.name] = None
      self.check_single_extension(flank, a)
    else:
      if flank.is_extended(a):
        self.extensions[flank.name] = a

  def parse(self, src, contigs):
    alignments = []
    read_count = 0
    for i in src:
      #print(i.rstrip())
      if i[0] != '#':
        cols = i.strip().split('\t')
        if cols[1] in self.flankmap:
          if self.flankmap[cols[1]].contig.name in contigs:
            self.identify_overlaps(cols, self.flankmap[cols[1]])
        read_count += 1
    for i in self.extensions:
      print(i, self.extensions[i].read.sra_rowid)
      alignments.append(self.extensions[i])
    print("Overlapping reads: {}/{}".format(len(alignments), read_count))
    return alignments
