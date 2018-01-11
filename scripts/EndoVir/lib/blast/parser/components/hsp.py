#  hsp.py
#
#  Copyright 2017 The University of Sydney
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0

class Hsp:

  def __init__(self, blast_hsp, query, hit, count):
    self.bitscore =  float(blast_hsp.get('bit_score', 0))
    self.num = int(blast_hsp.get('num', 0))
    self.score = int(blast_hsp.get('score', 0))
    self.evalue = float(blast_hsp.get('evalue', 100))
    self.identity = int(blast_hsp.get('identity', 0))
    self.positive = int(blast_hsp.get('positive', 0))
    self.alength = int(blast_hsp.get('align_len', 0))
    self.gaps = int(blast_hsp.get('gaps', 0))
    self.query_strand = blast_hsp.get('query_strand', 'NA')
    self.hit_strand = blast_hsp.get('hit_strand', 'NA')
    self.hit_from = int(blast_hsp.get('hit_from', 0)) - 1
    self.hit_to = int(blast_hsp.get('hit_to', 0)) - 1
    self.query_from = int(blast_hsp.get('query_from', 0)) - 1
    self.query_to = int(blast_hsp.get('query_to', 0)) - 1
    self.hseq = blast_hsp.get('hseq')
    self.qseq = blast_hsp.get('qseq')
    self.hid = count
    self.query = query
    self.hit = hit
