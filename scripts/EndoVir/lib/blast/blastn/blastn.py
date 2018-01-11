#  blastn.py
#
#  Copyright 2017 USYD
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import os
import sys
import subprocess

sys.path.insert(1, os.path.join(sys.path[0], '../../'))

class BlastN:

  def __init__(self, path='blastn'):
    self.path = path
    self.num_threads = 4
    self.outfmt = 15

  def run(self, db, query):
    cmd = [self.path, '-db',  db,
                      '-num_threads', str(self.num_threads),
                      '-outfmt', str(self.outfmt)]
    print(cmd)
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=query, bufsize=1,
                            universal_newlines=True)
