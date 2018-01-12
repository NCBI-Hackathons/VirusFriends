#  consensus.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import io
import sys

class Consenter:

  def __init__(self):
    self.reference = None
    self.refname = None
    self.mtx = []


  def add_ref(self, ref):
    fh = open(ref, 'r')
    for i in fh:
      if i[0] == '>':
        self.refname = i[1:].strip()
        self.reference = ''
        continue
      self.reference += i.strip()
    self.mtx = [{x:1} for x in self.reference]
    #print(len(self.mtx), self.mtx)

  def make_consensus(self):
    cons = ''
    for i in self.mtx:
      s = [(k, i[k]) for k in sorted(i, key=i.get, reverse=True)]
      cons += s[0][0]
    return ">{}\n{}".format(self.refname+'_cons', cons)

  def isInt(self, char):
    if ord(char) >= 48 and ord(char) <= 57:
      return True
    return False

  def isGap(self, char):
    if ord(char) == 45:
      return True
    return False

  def isLetter(self, char):
    if ord(char) >= 65 and ord(char) <= 90:
      return True
    return False

  def decode_btop(self, cols):
    #print(cols)
    refpos = int(cols[8])-1
    if cols[8] > cols[9]:
      refpos = int(cols[9])-1
    num = ''
    status = 0
    btop_idx = 0
    btop = cols[16]+" "
    mismatch = ''

    nextChar = True
    while nextChar:
      char = btop[btop_idx].upper()
      while status == 0:
        #print("Status: {0}:\trefpos {1}, BTOP: {2}".format(status, refpos, char), end = '\t')
        if self.isInt(char):
          status = 1
          #print("Switching to {0}".format(status))
          break
        if self.isLetter(char):
          btop_idx += 1
          mismatch = char + btop[btop_idx].upper()
          status = 2
          #print("Switching to {0}".format(status))
          break
        if self.isGap(char):
          btop_idx += 1
          mismatch = char + btop[btop_idx].upper()
          status = 2
          #print("Switching to {0}".format(status))
          break
        if ord(char) == 32:
          #print("Done. Checked BTOP: {0}".format(btop))
          nextChar = False
          break
        print("Unknown operation: {}".format(char), file=sys.stderr)

      while status == 1:
        #print("Status: {0}".format(status), end='\t')
        if self.isInt(char):
          num += char
          btop_idx += 1
          char = btop[btop_idx].upper()
          #print("Collecting int {0} at refpos {1}".format(num, refpos))
        else:
          for i in range(refpos, refpos+int(num), 1):
            self.mtx[i][self.reference[i]] += 1
          #print("Same nucs from {0}-{1}".format(refpos, refpos+int(num)), end='\t')
          refpos = i+1
          #print("Set refpos to {0}. Switching to {1}".format(refpos, 0))
          num = ''
          status = 0
          break

      while status == 2:
        if mismatch[0] == '-':
          #print("Gap in Ref")
          if mismatch[0] not in self.mtx[refpos]:
            self.mtx[refpos][mismatch[0]] = 0
          self.mtx[refpos][mismatch[0]] += 1
          refpos += 1
          status = 0
          btop_idx += 1
          break
        if mismatch[1] == '-':
          #print("Gap in Qry")
          refpos += 2
          status = 0
          btop_idx += 1
          break

        #print("Mismatch: pos {}, ref:{}, qry:{}".format(refpos, mismatch[1], mismatch[0]))
        if mismatch[0] not in self.mtx[refpos]:
          self.mtx[refpos][mismatch[0]] = 0
        self.mtx[refpos][mismatch[0]] += 1
        refpos += 1
        status = 0
        btop_idx += 1
        break


  def parse(self, src):
    for i in src:
      self.decode_btop(i.decode().strip().split('\t'))
