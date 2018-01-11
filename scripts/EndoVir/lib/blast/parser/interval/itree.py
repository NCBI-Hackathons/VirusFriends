#  itree.py
#
#  Copyright 2017 The University of Sydney
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#  based on http://www.geeksforgeeks.org/interval-tree/
#  Version: 0

import os
import base64

from . import interval

class Region:

  def __init__(self):
    self.start = 0
    self.stop  = 0
    self.intervals = []

class Itree:

  def __init__(self, ival):
    self.left = None
    self.right = None
    self.ival = ival
    self.upper = ival.upper
    self.anc = ''
    self.name = base64.urlsafe_b64encode(os.urandom(8)).decode()

  def insert(self, ival):

    if  ival.lower < self.ival.lower:
      if self.left is None:
        self.left = Itree(ival)
        self.left.anc = self.name
      else:
        self.left.insert(ival)
    else:
      if self.right is None:
        self.right = Itree(ival)
        self.right.anc = self.name
      else:
        self.right.insert(ival)

    if self.upper < ival.upper:
      self.upper = ival.upper


  def retrieve(self, container):
    if self.left:
      self.left.retrieve(container)
    container.append(self.ival)
    if self.right:
      self.right.retrieve(container)

  def traverse(self):
    if self.left:
      self.left.traverse()
    #print("[{0}, {1}] max = {2}, anc={3}, name={4}".format(self.ival.lower, self.ival.upper, self.upper, self.anc, self.name))
    if self.right:
      self.right.traverse()

  def hasOverlap(self, ivalA, ivalB):
    if (ivalA.lower <= ivalB.upper) and (ivalB.lower <= ivalA.upper):
      return True
    return False
