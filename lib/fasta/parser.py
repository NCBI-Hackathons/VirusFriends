#  parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
from . import sequence

class FastaParser:

  def __init__(self):
    self.sequences = {}
    self.doFhClose = False
    self.src = sys.stdin

  def parse(self, src=None, fil=None, stream=False):
    if fil != None:
      src = open(fil, 'r')
      self.doFhClose = True
    if src == None:
      print('Fasta parser. Error. No source to parse')
    seq = ''
    header = ''
    for i in src:
      if i[0] == '>':
        if len(seq) > 0:
          self.add_sequence(sequence.FastaSequence(header, seq), stream)
          seq = ''
        header = i[1:].strip()
      else:
        seq += i.strip()
    self.add_sequence(sequence.FastaSequence(header, seq), stream)

    if self.doFhClose == True:
      src.close()

  def write_file(self, fname):
    fh = open(fname, 'w')
    for i in self.sequences:
      fh.write(self.sequences[i].get_sequence())
    fh.close()
    return fname

  def add_sequence(self, seq, stream):
    if stream == True:
      print(seq.get_sequence())
    self.sequences[seq.header] = seq

  def reset(self):
    self.sequences = {}
