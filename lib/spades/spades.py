#  spades.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import subprocess

from ..fasta import parser

class Spades:

  def __init__(self, path='spades.py'):
    self.path = path
    self.suffix = ".contigs.fa"
    self.min_contig_len = 400
    self.parser = parser.FastaParser()

  def run(self, reads, prefix=None, outdir='asm', cpu_threads=4):
    self.parser.reset()
    cmd = [self.path, '-s',
                      '-i', reads,
                      '--meta',
                      '-t', str(cpu_threads),
                      '-m', '12']

    if prefix == None:
      prefix = reads
    cmd += ['-o', outdir]
    print("Log", cmd)
    spades = subprocess.run(cmd)
    fil=os.path.join(outdir, prefix+self.suffix)
    print ("Spades finished with %s, file is %s" % (spades, fil))

    self.parser.parse(fil)
    return os.path.join(outdir, prefix+self.suffix)

  def new(self):
    return Spades()
