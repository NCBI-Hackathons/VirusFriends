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
import logging as log

verbose = False

class VirusFriends:

    def __init__(self, wd=None, virusdb=None, cdddb=None):
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
        #chnaged the code back to endovir
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
        self.check_databases()
        if verbose:
            sys.stderr.write("Completed database setup\n")

    def check_databases(self):
        #Chnaging this code back to endovir code
        if not os.path.isdir(os.path.join(self.wd, self.dbs_dirname)):
           os.mkdir(os.path.join(self.wd, self.dbs_dirname))
        for i in self.db_sources:
           print("Setup Blast DB {0}".format(i), file=sys.stderr)
           self.dbs[i] = self.db_sources[i]['db']
           self.dbs[i].setup(src=self.db_sources[i]['src'])

    def screen(self, inputs=[], intype="srr"):
        vrs_ctgs = {}
        blastcmds = []
        if (intype == "srr"):
            blastcmds.append("-srr")
        elif (intype == "fasta"):
            blastcmds.append("-query")
        elif (intype == "fastq"):
            blastcmds.append(["infmt", "fastq", "-query"])
        else:
            raise ValueError("Input type %s isn't supported; try srr, fasta or fastq, please." % intype)
        for i in inputs:
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
            if (os.path.isfile(samfile) > 0):
                print("There's already a sam file at %s, skipping magicblast." % samfile)
            else:
                print("Could not find samfile at location %s, running magicblast." % samfile)
                s.screen_srr(s.srr, s.virus_db.path, samfile)
                #srr_alignments = s.screen_srr(i, s.virus_db.path)
                #vdb_parser = s.vdbdump.run(s.srr, srr_alignments)
            
            samfile = os.path.join(wd,"magicblast.sam")

            print("sam is %s and current working dir is %s" % (samfile, wd))
            sortit = s.sort_matches(samfile, wd)

            # vdb_parser = s.vdbdump.run(s.srr, srr_alignments)
            # contigs = s.assemble(vdb_parser.dump_to_file())
            weak_fasta = os.path.join(wd, "weak_%s.fasta" % i)
            contigs = s.assemble(weak_fasta)
            #print("contigs returns %s" % contigs)
            sys.exit(0)

            putative_virus_contigs = s.cdd_screen(contigs, s.cdd_db.path, os.path.join(s.wd, 'rpst'))

            if len(putative_virus_contigs) > 1000:
                for j in putative_virus_contigs:

                    print ("working on contig # j %s" % s.assembler.parser.sequences)
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
    ap.add_argument('-i', '--inputs', type=str, nargs='*',  default=['SRR5150787'], required=True,
                    help='One or more SRR numbers or fastq/a file paths as input, e.g. SRR5150787 or testfile.fq'),
    ap.add_argument('-t', '--intype', type=str, default='srr',
                    help='Type of input provided - can be either srr, fasta or fastq')
    ap.add_argument('-d', '--wd', type=str, default='analysis',
                    help='Working directory for analysis')
    ap.add_argument('-m', '--max_cpu', '-p', type=int, default=1,
                    help='Max number of cores to use. NOT YET IMPLEMENTED')
    ap.add_argument('-w', '--weak_threshold', type=int, default=80,
                    help='Threshold (in %% identity) to call a weak hit to the database. Default 80. Allowed: 1-100%%')
    ap.add_argument('-s', '--strong_threshold', type=int, default=70,
                    help='Threshold (in %% identity) to call a strong hit to the database. Default 70. Allowed: 1-100%%')
    ap.add_argument('-n', '--min_matched', type=int, default=50,
                    help='Minimum number of bases that must match to be considered a hit. Default 50. Allowed: 1- <readlength>')
    ap.add_argument('-b', '--database', type=str, default=None,
                    help='Database to use. Default is to download and install the RefSeq viral database')
    ap.add_argument('-v', '--verbose', help='verbose output (mostly for debugging)', action='store_true')
    args = ap.parse_args()

    global verbose
    ### Refactor all print statements that just help debug into log.debug("blah blah") instead of print("blah blah")
    if args.verbose:
        log.basicConfig(format='%(message)s',level=log.DEBUG)
        verbose = True

    # srrs = ['SRR5150787', 'SRR5832142']
    if args.inputs == ['SRR5150787']:
        print("Running test in {} using {}".format(args.wd, args.inputs))
    else:
        print("Analyzing  {} using {}.".format(args.inputs, args.wd), file=sys.stderr)

    e = VirusFriends(wd=args.wd, virusdb=args.database)
    if verbose:
        print("Checking databases", file=sys.stderr)
    e.setup()
    if verbose:
        print("Starting screen", file=sys.stderr)
        
    e.screen(args.inputs, args.intype)
    return 0


if __name__ == '__main__':
    main()
