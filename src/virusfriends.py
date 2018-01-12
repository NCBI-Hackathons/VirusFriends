#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  virusfriends.py
#
#  Authors:
#    Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#    Carrie Ganote <cganote@iu.edu>
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

verbose = False

class VirusFriends:

    def __init__(self, wd=None, virusdb=None):
        """
        Initialize the class
        :param wd: working directory
        :param virusdb: the virus database
        """
        self.analysis_path = ''
        self.dbs_path = ''
        self.wd = os.getcwd() if wd is None else wd
        self.screens = {}
        self.flank_len = 500
        self.dbs_dirname = 'dbs'
        self.db_sources = {
            'virusdb': {'src': ['ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.1.genomic.fna.gz',
                                'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.2.1.genomic.fna.gz'],
                        'db': lib.blast.blastdb.makeblastdb.Makeblastdb(name='viral.genomic.refseq.fna',
                                                                        dbdir=os.path.join(self.wd, self.dbs_dirname),
                                                                        typ='nucl')},
            'cdd': {'src': ['ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz'],
                    'db': lib.blast.blastdb.makeprofiledb.Makeprofiledb(name='endovir_cdd',
                                                                        dbdir=os.path.join(self.wd, self.dbs_dirname),
                                                                        typ='rps')}
        }

        if None == virusdb:
            self.db_sources['virusdb'] = {'src': ['ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.1.genomic.fna.gz',
                                                  'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.2.1.genomic.fna.gz'],
                                          'db': lib.blast.blastdb.makeblastdb.Makeblastdb(
                                              name='viral.genomic.refseq.fna',
                                              dbdir=os.path.join(self.wd, self.dbs_dirname),
                                              typ='nucl')}
        else:
            self.db_sources['virusdb'] = {'src' : [virusdb],
                                          'db'  : lib.blast.blastdb.makeblastdb.Makeblastdb(
                                              name=os.path.split(virusdb)[1],
                                              dbdir=os.path.join(os.path.split(virusdb)[0]),
                                              typ='nucl')
                                          }
        self.dbs = {}

    def set_wd(self):
        if not os.path.isdir(self.wd):
            os.mkdir(self.wd)

    def setup(self):
        self.set_wd()
        self.setup_databases()
        if verbose:
            sys.stderr.write("Completed database setup\n")

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
            wd = os.path.join(self.wd, i)
            ### Need to figure out if the current input (i) is a file or an srr accession #.
            intype = "srr"
            if ('.' in i or not "SRR" in i[0:2]):
                print ("Input file detected: %s" % i)
                intype = "query"
            ### Added logic here that checks for the existence of the sam file,
            ###  and runs magicblast if it isn't there or is size 0
            sambasename = "%s.sam" % i
            samfile = os.path.join(wd, sambasename)
            if (os.path.isfile(samfile) and os.path.getsize(samfile) > 0):
                print("There's already a sam file at %s, skipping magicblast." % samfile)
            else:
                print("Could not find samfile at location %s, running magicblast." % samfile)
                s.screen_srr(s.srr, s.virus_db.path, samfile)
            # srr_sam = os.path.join(wd,"magicblast.sam")

            print("sam is %s and current working dir is %s" % (samfile, wd))
            sortit = s.sort_matches(samfile, wd)

            # vdb_parser = s.vdbdump.run(s.srr, srr_alignments)
            # contigs = s.assemble(vdb_parser.dump_to_file())
            weak_fasta = os.path.join(wd, "weak_%s.fasta" % i)
            contigs = s.assemble(weak_fasta)
            print("contigs returns %s" % contigs)
            sys.exit(0)

            putative_virus_contigs = s.cdd_screen(contigs, s.cdd_db.path, os.path.join(s.wd, 'rpst'))
            if len(putative_virus_contigs) > 0:
                for j in putative_virus_contigs:
                    c = virus_contig.VirusContig("ctg_" + str(len(vrs_ctgs)),
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
    ap = argparse.ArgumentParser(description='Virus_Friends')
    ap.add_argument('-inputs', type=str, nargs='*',  default=['SRR5150787'],
                    help='One or more SRR numbers or fastq/a file paths as input, e.g. SRR5150787 or testfile.fq'),
    ap.add_argument('--wd', type=str, default='analysis',
                    help='Working directory for analysis')
    ap.add_argument('--max_cpu', '-p', type=int, default=1,
                    help='Max number of cores to use. NOT YET IMPLEMENTED')
    ap.add_argument('--weak_threshold', type=int, default=80,
                    help='Threshold (in % identity) to call a weak hit to the database. Default 80. Allowed: 1-100 (%)')
    ap.add_argument('--strong_threshold', type=int, default=70,
                    help='Threshold (in % identity) to call a strong hit to the database. Default 70. Allowed: 1-100 (%)')
    ap.add_argument('--min_matched', type=int, default=50,
                    help='Minimum number of bases that must match to be considered a hit. Default 50. Allowed: 1- <readlength>')
    ap.add_argument('-db', type=str, default=None,
                    help='Database to use. Default is to download and install the RefSeq viral database')
    ap.add_argument('-verbose', help='verbose output (mostly for debugging)', action='store_true')
    args = ap.parse_args()

    global verbose
    if args.verbose:
        verbose = True

    # srrs = ['SRR5150787', 'SRR5832142']
    if args.inputs == ['SRR5150787']:
        print("Running test in {} using {}".format(args.wd, args.inputs), file=sys.stderr)
    else:
        print("Analyzing  {} using {}.".format(args.inputs, args.wd), file=sys.stderr)

    e = VirusFriends(wd=args.wd, virusdb=args.db)
    if verbose:
        print("Checking databases", file=sys.stderr)
    e.setup()
    if verbose:
        print("Starting screen", file=sys.stderr)
    e.screen(args.inputs)
    return 0


if __name__ == '__main__':
    main()
