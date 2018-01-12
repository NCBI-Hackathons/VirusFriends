#  megahit.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import subprocess

from ..fasta import parser

class Megahit:

  def __init__(self, path='megahit'):
    self.path = path
    self.suffix = ".contigs.fa"
    self.min_contig_len = 400
    self.parser = parser.FastaParser()

  def run(self, reads, prefix=None, outdir='megahit_out', cpu_threads=4):
    self.parser.reset()
    cmd = [self.path, '--read', reads,
                      '--num-cpu-threads', str(cpu_threads),
                      '--min-contig-len', str(self.min_contig_len),
                      '--keep-tmp-files']
    if prefix == None:
      prefix = reads
    cmd += ['--out-prefix', prefix, '--out-dir', outdir]
    print("Log", cmd)
    megahit = subprocess.call(cmd)
    self.parser.parse(fil=os.path.join(outdir, prefix+self.suffix))
    return os.path.join(outdir, prefix+self.suffix)

  def new(self):
    return Megahit()
