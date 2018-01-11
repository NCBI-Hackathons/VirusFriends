#  blast_json.py
#
#  Copyright 2017 The University of Sydney
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#   A blast parsre for results in JSON


import os
import sys
import json
import hashlib

from .components import query
from .components import hit
from .components import hsp
from .interval import itree
from .interval import interval

class BlastParser:

  def __init__(self):
    self.querymap = {}
    self.query_ivals = {}
    self.hit_ivals = {}
    self.hitmap = {}
    self.hspmap = {}
    self.edges = {}
    self.hsp_count = 0

  def parse(self, stdin):
    blast_result = json.load(stdin)
    for i in blast_result['BlastOutput2']:
      self.parse_results(i['report']['results'])


  def parse_results(self, results):
    bl_query = self.add_query(query.BlastQuery(results['search']['query_id'],
                                               results['search']['query_title'],
                                               results['search']['query_len']))

    if len(results['search']['hits']) > 0:
      self.add_hits(results['search']['hits'], bl_query)

  def add_hits(self, hits, bl_query):
    for i in hits:
      bl_hit = self.add_hit(hit.BlastHit(i['description'][0]['id'],
                                         i['description'][0]['accession'],
                                         i['description'][0]['title'],
                                         i['len'],
                                         i['num']))
      for j in i['hsps']:
        h = self.add_hsp(hsp.Hsp(j, bl_query, bl_hit, self.hsp_count))
        qival = interval.Interval(j['query_from'], j['query_to'], "qry"+str(j['num']))
        hival = interval.Interval(j['hit_from'], j['hit_to'], "hit"+str(j['num']))
        hival.connect(qival, h)
        bl_hit.intervals.insert(hival)
        qival.connect(hival, h)
        bl_query.intervals.insert(qival)
        self.hsp_count += 1

  def add_hsp(self, hsp):
    if hsp.hid not in self.hspmap:
      self.hspmap[hsp.hid] = hsp
    return hsp


  def add_query(self, query):
    if query.qid not in self.querymap:
      self.querymap[query.qid] = query
    return self.querymap[query.qid]

  def add_hit(self, hit):
    if hit.hid not in self.hitmap:
      self.hitmap[hit.hid] = hit
    return self.hitmap[hit.hid]

  def show_queries(self):
    for i in self.querymap:
      self.querymap[i].dump()

  def show_hits(self):
    for i in self.hitmap:
      self.hitmap[i].dump()

  def reset(self):
    self.querymap = {}
    self.query_ivals = {}
    self.hit_ivals = {}
    self.hitmap = {}
    self.hspmap = {}
    self.edges = {}
    self.hsp_count = 0
