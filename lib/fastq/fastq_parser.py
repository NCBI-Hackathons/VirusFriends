#  fastq_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from ..sequence import sequence

class FastqParser:

  def __init__(self):
    self.sequences = {}

  def parse(self, src):
    line_count = 1
    header = ''
    seq = ''
    qual = ''
    for i in src:
      if line_count == 1:
        header = i.strip()[1:]
      if line_count == 2:
        seq = i.strip()
      if line_count == 4:
        qual = i.strip().decode()
        sequences[header] = sequence.FastqSequence(header, seq, qual)
        line_count = 0
      line_count += 1

  def reset(self):
    self.sequences = {}

  def dump_to_file(self, fout=None):
    if fout == None:
      fout = 'dump.fq'
    fh = open(fout, 'w')
    for i in self.sequences:
      fh.write(self.sequences[i].get_sequence()+'\n')
    fh.close()
    return fout
