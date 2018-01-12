#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  endovir.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import os
import sys
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.blastdb.makeblastdb
import lib.blast.blastdb.makeprofiledb

import screener
import virus_contig

class Endovir:

  def __init__(self, wd=None):
    self.analysis_path = ''
    self.dbs_path = ''
    self.wd = os.getcwd() if wd is None else wd
    self.screens = {}
    self.flank_len = 500
    self.dbs_dirname = 'dbs'
    self.db_sources = {
      'virusdb' : {'src' : ['ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.1.genomic.fna.gz',
                            'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.2.1.genomic.fna.gz'],
                   'db' : lib.blast.blastdb.makeblastdb.Makeblastdb(name='viral.genomic.refseq.fna',
                                                                    dbdir=os.path.join(self.wd, self.dbs_dirname),
                                                                    typ='nucl')},
      'cdd' : {'src' : ['ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz'],
               'db' : lib.blast.blastdb.makeprofiledb.Makeprofiledb(name='endovir_cdd',
                                                                    dbdir=os.path.join(self.wd, self.dbs_dirname),
                                                                    typ='rps')}
    }
    self.dbs = {}


  def set_wd(self):
    if not os.path.isdir(self.wd):
      os.mkdir(self.wd)

  def setup(self):
    self.set_wd()
    self.setup_databases()

  def setup_databases(self):
    if not os.path.isdir(os.path.join(self.wd, self.dbs_dirname)):
      os.mkdir(os.path.join(self.wd, self.dbs_dirname))
    for i in self.db_sources:
      print("Setup Blast DB {0}".format(i), file=sys.stderr)
      self.dbs[i] = self.db_sources[i]['db']
      self.dbs[i].setup(src=self.db_sources[i]['src'])

  def screen(self, srrs=[]):
    vrs_ctgs = {}
    for i in srrs:
      print("Screening {0}".format(i), file=sys.stderr)
      s = screener.Screener(self.wd, i, self.dbs['virusdb'], self.dbs['cdd'])
      #srr_alignments = s.screen_srr(s.srr, s.virus_db.path)
      srr_sam = s.screen_srr(s.srr, s.virus_db.path)
      sortit = s.sort_matches(srr_sam, self.wd)
      exit(0)
      #vdb_parser = s.vdbdump.run(s.srr, srr_alignments)
      contigs = s.assemble(vdb_parser.dump_to_file())
      putative_virus_contigs = s.cdd_screen(contigs, s.cdd_db.path, os.path.join(s.wd, 'rpst'))
      if len(putative_virus_contigs) > 0:
        for j in putative_virus_contigs:
          c = virus_contig.VirusContig("ctg_"+str(len(vrs_ctgs)),
                                      s.assembler.parser.sequences[j].sequence,
                                      i,
                                      s.assembler.parser.sequences[j].header,
                                      self.flank_len,
                                      s.wd)
          vrs_ctgs[c.name] = c
          print("Prepared {} for budding".format(c.name))
        print("Budding {} contigs".format(len(vrs_ctgs)))
        s.bud(vrs_ctgs)
      else:
        print("No contigs with virus motifs detected")
        sys.exit()

def main():
  ap = argparse.ArgumentParser(description='Endovir')
  ap.add_argument('-srr', type=str, default='SRR5150787',
                  help='SRR number, e.g. SRR5150787'),
  ap.add_argument('--wd', type=str, default='analysis',
                  help='Working directory for analysis')
  ap.add_argument('--max_cpu', '-p', type=int, default=1,
                  help='Max number of cores to use. NOT YET IMPLEMENTED')
  args = ap.parse_args()
  #srrs = ['SRR5150787', 'SRR5832142']
  if args.srr == 'SRR5150787':
    print("Running test in {} using {}".format(args.wd, args.srr), file=sys.stderr)
  else:
    print("Analyzing  {} using {}.".format(args.srr, args.wd), file=sys.stderr)
  e = Endovir(wd=args.wd)
  print("Checking databases", file=sys.stderr)
  e.setup()
  print("Starting screen", file=sys.stderr)
  e.screen([args.srr])
  return 0

if __name__ == '__main__':
  main()
