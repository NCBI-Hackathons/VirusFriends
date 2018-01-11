#!/usr/bin/env python3
#  makeprofiledb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0
import os
import subprocess
from . import database

class Makeprofiledb(database.BlastDatabase):

  def __init__(self, dbdir, name, typ):
    super().__init__(dbdir=dbdir, name=name, typ=typ, cmd='makeprofiledb')

  def make_db(self, pssms):
    cmd = self.cmd + ['-dbtype', self.typ,
                      '-in', pssms,
                      '-out', os.path.join(self.dbdir, self.title),
                      '-title', self.title,
                      '-threshold',  '9.82',
                      '-scale', '100',
                      '-index', 'true'
                      ]
    print(cmd)
    subprocess.run(cmd)
