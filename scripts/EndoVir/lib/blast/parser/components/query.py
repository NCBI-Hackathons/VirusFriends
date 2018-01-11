#  blast_query.py
#
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#

import hashlib
from ..interval import itree
from ..interval import interval

class BlastQuery:

  def __init__(self, id='', title='', length=0):
    self.id = id
    self.title = title
    self.length = length
    self.qid = hashlib.md5(title.encode()).hexdigest()
    self.intervals = itree.Itree(interval.Interval(0, length, "qry"+str(0)))

  def dump(self):
    print("Qid: {0}\nId: {1}\nTitle: {2}\nLength: {3}".format(self.qid,
                                                              self.id,
                                                              self.title,
                                                              self.length))

  def get_intervals(self):
    intervals = []
    self.intervals.retrieve(intervals)
    return intervals
