#  flank.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.sequence.sequence
import extensions.extension

class BlastData:

  def __init__(self):
    self.start = 0
    self.stop = 0
    self.strand = "Plus"

  def update(self, start, stop, strand):
    self.start = int(start)
    self.stop = int(stop)
    self.strand = strand

class Flank:

  def __init__(self, ctg, side):
    self.contig = ctg
    self.length = ctg.flank_len
    self.side = side
    self.name = "{}_{}".format(self.contig.name, self.side)
    self.start = 0
    self.stop = 0
    self.ref_overlap = 5
    self.qry_overlap = 20
    self.shift = 0
    self.extension = extensions.extension.Extension(self)
    self.calculate_coordinates()
    self.blast_data = BlastData()

  def has_extension(self):
    if self.extension.length == 0:
      return False
    return True

  def is_extended(self, alignment):
    raise NotImplementedError("Require  check_overlap() implementation")

  def get_fasta_sequence(self):
    raise NotImplementedError("Require get_fasta_sequence() implementation")

  def calculate_coordinates(self, contig):
    raise NotImplementedError("Require calculate_coordinates() implementation")

  def show(self):
    print("\t{}\t{} :\t{}\t{}\t{}\t{}".format(self.side,
                                         self.name,
                                         self.start,
                                         self.stop,
                                         self.length,
                                         self.shift))
