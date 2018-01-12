#  flankdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../../'))
import lib.sequence
import lib.blast.blastdb.database


class FlankDb(lib.blast.blastdb.makeblastdb.Makeblastdb):

  def __init__(self, dbdir, dbname):
    super().__init__(dbdir=dbdir, name=dbname, typ='nucl')
    self.flankmap = {}

  def collect_flanks(self, contigs):
    self.flankmap = {}
    rfd, wfd = os.pipe()
    stdout = os.fdopen(wfd, 'w')
    for i in contigs:
      print()
      stdout.write(contigs[i].get_flanks())
      self.flankmap[contigs[i].lhs_flank.name] = contigs[i].lhs_flank
      if contigs[i].hasRhsFlank:
        self.flankmap[contigs[i].rhs_flank.name] = contigs[i].rhs_flank
    stdout.close()
    stdin = os.fdopen(rfd, 'r')
    self.make_db_stdin(stdin)
    stdin.close()
    return True
