#  flank_checker.py
#
#  Copyright 2017 USYD
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import io
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.parser.blast_json

class FlankChecker(lib.blast.parser.blast_json.BlastParser):

  def __init__(self):
    super().__init__()
    self.updates = {}

  def check(self, contigs, lnk):
    for i in self.hspmap:
      flankA = lnk.get_flank(self.hspmap[i].query.title)
      flankB = lnk.get_flank(self.hspmap[i].hit.accession)
      print("Blast results: {} vs. {}".format(flankA.name, flankB.name))
      if flankA.contig.name != flankB.contig.name:
        print("Checking {} and {} for overlap".format(flankA.name, flankB.name))
        flankA, flankB = self.check_updated_flanks(flankA, flankB)
        print(flankA.contig.name, flankB.contig.name)
        if flankA.contig.name == flankB.contig.name:
          continue
        flankA.blast_data.update(self.hspmap[i].query_from, self.hspmap[i].query_to, self.hspmap[i].query_strand)
        flankB.blast_data.update(self.hspmap[i].hit_from, self.hspmap[i].hit_to, self.hspmap[i].hit_strand)
        if flankA.blast_data.strand == flankB.blast_data.strand:
          self.update_contig_map(contigs, self.merge_same_strand(flankA, flankB))
        else:
          self.update_contig_map(contigs, self.merge_different_strand(flankA, flankB))
      else:
        if flankA.name != flankB.name:
          raise NotImplementedError("Smells like circular or terminal repeat business. \
                                      Not yet implemented. How about now?")
        else:
          print("Not an overlap")

  # I don't understand why it explicitly requires a return
  def check_updated_flanks(self, flankA, flankB):
    if flankA.contig.name in self.updates:
      print("\tUpdate: {} is now {}".format(flankA.contig.name, self.updates[flankA.contig.name].name))
      if flankA.side == 'rhs':
        flankA = self.updates[flankA.contig.name].rhs_flank
      else:
        flankA = self.updates[flankA.contig.name].lhs_flank

    if flankB.contig.name in self.updates:
      print("\tUpdate: {} is now {}".format(flankB.contig.name, self.updates[flankB.contig.name].name))
      if flankB.side == 'rhs':
        flankB = self.updates[flankB.contig.name].rhs_flank
      else:
        flankB = self.updates[flankB.contig.name].lhs_flank
    return (flankA, flankB)

  def merge_same_strand(self, flankA, flankB):
    if flankA.side == 'rhs' and flankB.side == 'lhs':
      print("{}:{} + {}:{}".format(flankA.contig.name, flankA.side, flankB.contig.name, flankB.side))
      flankA.contig.merge_contig_rhs(flankB.contig)
      return self.update_flank_map(flankA.contig, flankB.contig)

    if flankA.side == 'lhs' and flankB.side == 'rhs':
      print("{}:{} + {}:{}".format(flankB.contig.name, flankB.side, flankA.contig.name, flankA.side))
      flankB.contig.merge_contig_rhs(flankA.contig)
      return self.update_flank_map(flankB.contig, flankA.contig)

  def merge_diff_strand(self, flankA, flankB):
    print("One flank is on the other strand")
    raise NotImplementedError("Different strand overlap.\
                               Not yet implemented. How about now?")

  def update_contig_map(self, contigs, merged_contig):
    if merged_contig.name in contigs:
      print("rm: ", merged_contig.name)
      del contigs[merged_contig.name]
    for i in contigs:
      print(i, contigs[i].history)

  def update_flank_map(self, anchor_ctg, merged_ctg):
    print("Anchor: {}\tMerge: {}".format(anchor_ctg.name, merged_ctg.name))
    for i in self.updates:
      if self.updates[i].name == merged_ctg.name:
        print("DEBUG: value update")
        self.updates[i] = anchor_ctg
        anchor_ctg.history += self.updates[i].history
        #break
    if merged_ctg.name not in self.updates:
      self.updates[merged_ctg.name] = anchor_ctg
      anchor_ctg.history.append(merged_ctg.name)
    for i in self.updates:
      print("{} is merged in {}".format(i, self.updates[i].name))


    return merged_ctg
