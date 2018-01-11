#  contig.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import shutil
import pathlib

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.magicblast
import lib.process.process
import lib.vdbdump.vdbdump
import lib.sequence.sequence
import lib.fasta.parser

import flanks.flank_lhs
import flanks.flank_rhs

class VirusContig(lib.sequence.sequence.Sequence):

  def __init__(self, name, seq, srr, src, flank_len, screen_dir):
    super().__init__(name, seq)
    self.src = src
    self.srr = srr
    self.flank_len = flank_len
    self.iteration = 0
    self.wd = self.mk_wd(os.path.join(screen_dir, self.name))
    self.lhs_flank = flanks.flank_lhs.LhsFlank(self)
    self.rhs_flank = flanks.flank_rhs.RhsFlank(self)
    self.update_flanks()
    self.hasRhsFlank = True
    self.history = []

  def get_shift(self):
    return self.lhs_flank.shift + self.rhs_flank.shift

  def mk_wd(self, path):
    if os.path.exists(path):
      shutil.rmtree(path)
    if not os.path.isdir(path):
      os.mkdir(path)
    return path

  def update_flanks(self):
    if self.length <= self.flank_len:
      self.hasRhsFlank = False
      self.rhs_flank.length = 0
      self.lhs_flank.length = self.length

  def log_overlap_coords(self, flank):
    if flank.extension.isRevCompl:
      print("DOUBLE CHECK THIS")
    print(self.srr)
    print("Flank: {}\t{}\t{}\t{}\t{}\t{}\t{}".format(flank.name,
                                             flank.start,
                                             flank.stop,
                                             flank.length,
                                             flank.extension.alignment.flank.strand,
                                             flank.extension.alignment.flank.start,
                                             flank.extension.alignment.flank.stop))
    print("Read:  {}\t{}\t{}\t{}\t{}".format(flank.extension.sra_rowid,
                                             flank.extension.alignment.read.start,
                                             flank.extension.alignment.read.stop,
                                             flank.extension.alignment.read.length,
                                             flank.extension.alignment.read.strand))

    print("Ext:   {}\t{}\t{}".format(flank.extension.start,
                                     flank.extension.stop,
                                     flank.extension.length))


  def revcomp_seq(self, seq, beg, end):
    return seq[beg:end+1][::-1].translate(str.maketrans("ACTG", "TGAC"))

  def extend_lhs(self, flank, reads):
    if flank.extension.sra_rowid in reads:
      self.log_overlap_coords(flank)
      ext = None
      if flank.extension.isRevCompl:
        ext = self.revcomp_seq(reads[flank.extension.sra_rowid],
                                     flank.extension.alignment.read.stop,
                                     flank.extension.alignment.read.length)
      else:
        ext = reads[flank.extension.sra_rowid][:flank.extension.alignment.read.start]
      self.update_sequence(ext+self.sequence[flank.start+flank.extension.alignment.flank.start:], flank)

  def extend_rhs(self, flank, reads):
    if flank.extension.sra_rowid in reads:
      ext = None
      self.log_overlap_coords(flank)
      if flank.extension.isRevCompl:
        ext = self.revcomp_seq(reads[flank.extension.sra_rowid], 0, flank.extension.alignment.read.stop)
      else:
        ext = reads[flank.extension.sra_rowid][flank.extension.alignment.read.stop+1:]
      self.update_sequence(self.sequence[:flank.start+flank.extension.alignment.flank.stop+1]+ext, flank)




  def merge_contig_rhs(self, rhs_contig):
    print("LHS:\t{}\nRHS\t{}".format(self.lhs_flank.shift, self.rhs_flank.shift))
    print("oLHS:\t{}\noRHS\t{}".format(rhs_contig.lhs_flank.shift, rhs_contig.rhs_flank.shift))
    print("Src: {}\t{}".format(self.name, self.length))
    print(" RHS_flank: {}\t{}\t{}".format(self.rhs_flank.start, self.rhs_flank.stop, self.rhs_flank.length))
    print("  Extension: {}\t{}\t{}".format(self.rhs_flank.extension.start, self.rhs_flank.extension.stop, self.rhs_flank.extension.length))
    print("Dst: {}\t{}\t{}\t{}\t{}".format(rhs_contig.name, rhs_contig.length,
                                           rhs_contig.lhs_flank.blast_data.start, rhs_contig.lhs_flank.blast_data.stop,
                                           rhs_contig.lhs_flank.extension.start))
    print("Brk: {}\t{}\t{}\t{}".format(self.name, self.length-self.rhs_flank.length+self.rhs_flank.blast_data.start,
                                       rhs_contig.name, rhs_contig.lhs_flank.blast_data.start+rhs_contig.lhs_flank.shift))

    # update rhs side
    self.sequence = self.sequence[:self.length-self.rhs_flank.length+self.rhs_flank.blast_data.start] + \
                    rhs_contig.sequence[rhs_contig.lhs_flank.blast_data.start+rhs_contig.lhs_flank.shift:]
    shift = len(self.sequence) - self.length
    fh = open(self.name+rhs_contig.name, 'w')
    fh.write(self.sequence)
    fh.close()
    self.rhs_flank = flanks.flank_rhs.RhsFlank(self)
    self.rhs_flank.extension.start = rhs_contig.rhs_flank.extension.start + shift
    self.rhs_flank.extension.stop = rhs_contig.rhs_flank.extension.stop + shift
    self.rhs_flank.blast_data.start = shift
    self.rhs_flank.blast_data.stop = shift
    print("--------------------------------------------")

  def save_fasta(self):
    fh = open(os.path.join(self.wd, self.name+'.fa'), 'w')
    fh.write(">{}\n{}\n".format(self.name, self.sequence))
    fh.close()

  def extend(self, reads):
    if self.lhs_flank.has_extension():
      self.extend_lhs(self.lhs_flank, reads)
    if self.rhs_flank.has_extension():
      self.extend_rhs(self.rhs_flank, reads)

  def get_flanks(self):
    if self.hasRhsFlank:
      return self.lhs_flank.get_fasta_sequence() + self.rhs_flank.get_fasta_sequence()
    return self.lhs_flank.get_fasta_sequence()

  def update_sequence(self, new_seq, flank):
    flank.shift = len(new_seq) - self.length
    self.sequence = new_seq
    self.length = len(new_seq)
    if flank.side == 'lhs':
      self.rhs_flank.extension.shift_coordinates(flank.shift)
    self.rhs_flank.calculate_coordinates()

  def show(self):
    print("{}\t{}".format(self.name, self.length))
    self.lhs_flank.show()
    self.lhs_flank.extension.show()
    self.rhs_flank.show()
    self.rhs_flank.extension.show()
    print("-------------------")
