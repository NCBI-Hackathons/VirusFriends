#  extension.py
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>

class Extension:

  def __init__(self, flank):
    self.flank = flank
    self.length_to_extend = 0
    self.length_on_contig = 0
    self.length = 0
    self.start = 0
    self.stop = 0
    self.alignment = None
    self.side = flank.side
    self.isRevCompl = False
    self.name = "{}_{}".format(self.flank.name, "ext")
    self.sra_rowid = 0

  def is_longer_alignment(self, alignment):
    if self.calc_extension_length(alignment) > self.length_to_extend:
      self.length_to_extend = self.calc_extension_length(alignment)
      self.length_on_contig = abs(alignment.flank.stop-alignment.flank.start) + 1
      self.length = self.length_to_extend + self.length_on_contig
      self.alignment = alignment
      self.sra_rowid = alignment.read.sra_rowid
      self.strand_check()
      self.update_coordinates(alignment)
      return True
    return False

  def calc_extension_length(self, alignment):
    return alignment.read.length - abs(alignment.read.stop-alignment.read.start) + 1

  def get_contig(self):
    return self.flank.contig

  def strand_check(self):
    if self.alignment.flank.strand != self.alignment.read.strand:
      self.isRevCompl = True
    else:
      self.isRevCompl = False

  def update_coordinates(self, alignment):
    raise NotImplementedError("Require udpate_coordinates() implementation")


  def shift_coordinates(self, shift):
    raise NotImplementedError("Require shift_coordinates() implementation")

  def show(self):
    print("\t{} :\t{}\t{}\t{}\t{}\t{}\t{}".format(self.sra_rowid,
                                                  self.side,
                                                  self.start,
                                                  self.stop,
                                                  self.length_on_contig,
                                                  self.length_to_extend,
                                                  self.length))
