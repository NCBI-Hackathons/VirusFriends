#!/usr/bin/env python3
#  blastdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import gzip
import subprocess
import tarfile
import urllib.request
import time

from . import blastdbcmd


class BlastDatabase:
    def __init__(self, cmd=None, dbdir=None, name=None, typ=None):
        self.title = name
        self.dbdir = dbdir
        self.typ = typ
        self.dbtool = blastdbcmd.Blastdbcmd()
        self.path = os.path.join(self.dbdir, self.title)
        self.cmd = [cmd]

    def make_db(self, fil=None):
        # test and see if the database has already been formated
        dbcomplete = True
        for extn in ["nhd", "nhi", "nhr", "nin", "nog", "nsd", "nsi", "nsq"]:
            if not os.path.exists(os.path.join(self.dbdir, "{}.{}".format(self.title, extn))):
                dbcomplete = False
        if dbcomplete:
            sys.stderr.write("The database {} is complete. Not reformatting\n".format(self.title))
            return

        cmd = self.cmd + ['-dbtype', self.typ, '-in', fil, '-out', os.path.join(self.dbdir, self.title), '-title',
                          self.title]
        print(cmd)
        subprocess.run(cmd)

    def make_db_stdin(self, stdout):
        cmd = self.cmd + ['-dbtype', self.typ, '-out', os.path.join(self.dbdir, self.title), '-title', self.title]
        print(cmd)
        # p = subprocess.Popen(cmd, stdin=stdout)
        p = subprocess.Popen(cmd, stdin=stdout)
        while p.poll() == None:
            time.sleep(2)

        if p.returncode != 0:
            print("Creating db {} failed. Aborting.".format(self.title))
            raise RuntimeError()

    def setup(self, src):
        if os.path.exists(self.dbdir):
            if not self.dbtool.exists(os.path.join(self.dbdir, self.title)):
                print("No Blast DB {0}".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
                if not os.path.exists(os.path.join(os.path.join(self.dbdir, self.title))):
                    self.fetch_db(src, self.title)
                print("\tfound local data at {0}. Creating database".format(os.path.join(self.dbdir, self.title),
                                                                            file=sys.stderr))
                dbdir_title = os.path.join(self.dbdir, self.title)
                self.make_db(dbdir_title)
            else:
                print("\tfound local Blast DB {0}".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
        else:
            os.mkdir(self.dbdir)
            self.fetch_db(src, self.title)
            self.make_db(src)

    def fetch_db(self, src, title):
        if src == 'Cdd':
            return
        if not src.startswith('http') or not src.startswith('ftp'):
            sys.stderr.write("{} does not appear to be a URL from to which to fetch the file\n".format(src))
            return
        print("Fetching database {} from {}".format(title, src))
        db = open(self.path, 'w')
        for i in src:
            dbgz = open('dbgz', 'wb')
            response = urllib.request.urlopen(i)
            dbgz.write(response.read())
            dbgz.close()
            f = gzip.open('dbgz', 'rb')
            db.write(f.read().decode())
            os.unlink('dbgz')
        db.close()
        # print("DB fetch placeholder for {0} to make db {1}".format(src, title))
