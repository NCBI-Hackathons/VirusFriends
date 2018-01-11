#  hit.py
#
#  Copyright 2017 The University of Sydney
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  To store intervals an interval tree should work. And voila, NCBI's cpp tooit
#  does exactly that [0]
#
# [0]: https://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/doxyhtml/itree_8hpp_source.html#l00288
#

import hashlib
from ..interval import itree
from ..interval import interval

class BlastHit:

  def __init__(self, id='', accession='', title='', length=0, hitnum=0):
    self.id = id
    self.accession = accession
    self.title = title
    self.length = length
    self.num = hitnum
    self.hid = hashlib.md5((title+accession).encode()).hexdigest()
    self.intervals = itree.Itree(interval.Interval(0, length, "Hit"+str(0))) # interval trees at some point, (see [0])?


  def dump(self):
    print("Hid: {0}\nId: {1}\nTitle: {2}\Accession: {3}\nLength: {4}\nNumber{5}".format(self.hid,
                                                                           self.id,
                                                                           self.title,
                                                                           self.accession,
                                                                           self.length,
                                                                           self.num))
