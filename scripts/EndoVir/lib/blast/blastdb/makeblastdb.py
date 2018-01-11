#  makeblastdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os

from . import database

class Makeblastdb(database.BlastDatabase):

  def __init__(self, dbdir, name, typ):
    super().__init__(dbdir=dbdir, name=name, typ=typ, cmd='makeblastdb')
    self.cmd  = self.cmd + ['-parse_seqids', '-hash_index']
