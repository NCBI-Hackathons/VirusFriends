#!/bin/bash
#  \file setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \description Install and setup dependencies for VirusFriends
#  \version 0.0.2

## Setup and create basic paths
export VirusFriends=$PWD
VirusFriends_dbs="$VirusFriends/analysis/dbs"
mkdir -p $VirusFriends_dbs
VirusFriends_tools="$VirusFriends/tools"
mkdir -p $VirusFriends_tools
#BASEDIR=$PWD
NEWPATH=""

## Basic tools
wget=$(which wget)


## Global variables
TESTONLY=0
INSTALL=0
if [ "$1" == "-L" ]; then
  TESTONLY=1;
  echo "Only listing software to be installed"
elif [ "$1" == "-I" ]; then
  INSTALL=1;
  echo "Installing software"
else
  echo "
 `basename $0` [-LV]
-L: List the software that will be installed. No changes will be made.
-I: Install the software

This installer will test for several pieces of software in your path and optionally install those that are missing.

If you provide the -L option, it will just list the software that will be installed.

If you provide the -I option, it will download appropriate software and install it. The default installation
directory is $VirusFriends_tools, but you can edit this install script to change that if you would prefer.

Databases will also be installed in $VirusFriends_dbs.
"
  exit 0
fi

## essential functions

function isInPath()
{
 [[ ! -z $(which $1) ]] && return
}

function expand_newpath()
{
  NEWPATH=$NEWPATH:$1
}

## Load libaries
source $VirusFriends/setup/edirect_setup.sh
source $VirusFriends/setup/python_setup.sh
source $VirusFriends/setup/blast_setup.sh
source $VirusFriends/setup/samtools_setup.sh
source $VirusFriends/setup/spades_setup.sh




function make_endovir_cdd()
{

  if [ $TESTONLY == 1 ]; then echo "Making the VirusFriends CDD libraries"; fi
  if [ $INSTALL == 1 ]; then
    echo "" > "$VirusFriends_dbs/$endovir_pssms"
    local qry="txid10239[Organism:exp] NOT (predicted OR putative)"
    for i in $($esearch -db  cdd -query "$qry"                      | \
             $efetch -format docsum                               | \
             $xtract -pattern DocumentSummary -element Accession  | \
             grep -v cl)
      do
             echo $i".smp" >> "$VirusFriends_dbs/$endovir_pssms"
      done

    local cdd_ftp='ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz'
    wget $cdd_ftp -O - | tar -C "$VirusFriends_dbs/" -xzvT "$VirusFriends_dbs/$endovir_pssms"
    cd $VirusFriends_dbs
    makeprofiledb -title endovir -in $VirusFriends_dbs/Cdd.pn   \
                 -out $VirusFriends_dbs/endovir_cdd -dbtype rps -threshold 9.82 -scale 100 -index true
  fi
}


function make_viralrefseq_database()
{

        if [ $TESTONLY == 1 ]; then echo "Making the VirusFriends viral refseq database"; fi
        if [ $INSTALL == 1 ]; then
                echo "Making the VirusFriends viral refseq database";
    wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.1.genomic.fna.gz -O $VirusFriends_dbs/viral.genomic.fna.gz
                gunzip -d  $VirusFriends_dbs/viral.genomic.fna.gz
    makeblastdb -title viral.genomic.refseq.fna  -in $VirusFriends_dbs/viral.genomic.fna  \
        -out $VirusFriends_dbs/viral.genomic.refseq.fna -dbtype nucl -parse_seqids
        fi
}


function finish_up()
{
  if [ ! -z $NEWPATH ]; then
    NEWPATH=$(echo $NEWPATH | sed -e 's/^://')
    echo "You need to append $NEWPATH to your PATH environment variable."
    echo "I recommend doing this by adding the following line to ~/.bashrc"
    echo -e "\texport PATH=\$PATH:$NEWPATH"
    echo "but you may also want to add this to a different location so I didn't set it to you"
    export PATH=$NEWPATH:$PATH
  fi
}

setup_edirect
setup_python
setup_blast
setup_magicblast
setup_spades
#setup_sratoolkit
#setup_samtools

#make_endovir_cdd
#make_viralrefseq_database
#finish_up
