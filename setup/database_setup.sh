#!/bin/bash
#-------------------------------------------------------------------------------
#  \file database_setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.1
#  \description
#-------------------------------------------------------------------------------

function prepare_cdd_database()
{
  printf "" > $1  # reset pn file
  local cdd_smp_dir="$VirusFriends_dbs/cdd_smp"
  mkdir -p $cdd_smp_dir
  local cdd_db="endovir_cdd"
  local qry="txid10239[Organism:exp] NOT (predicted OR putative)"
  for i in $($esearch_bin -db cdd -query "$qry"| \
            $efetch_bin -format docsum                              | \
            $xtract_bin -pattern DocumentSummary -element Accession | \
            grep -v cl)
    do
            echo "$i.smp" >> "$1"
    done
  (set -x; $wget $2 -O - | tar -C "$cdd_smp_dir/" -xzvT $1 -f -)
  cd $cdd_smp_dir
  makeprofiledb -title endovir  \
                -in $1          \
                -out ../$cdd_db \
                -dbtype rps     \
                -threshold 9.82 \
                -scale 100      \
                -index true
  reset_wd
  return 0
}

function setup_cdd_database()
{
  if [ $TESTONLY == 1 ]
    then
      echo "Preparing the VirusFriends CDD libraries"
      return
  fi
  local cdd_pssms="$VirusFriends_dbs/endovir.pn"
  local cdd_ftp='ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz'
  prepare_cdd_database $cdd_pssms $cdd_ftp

  return
}

function prepare_viral_refseq_database()
{
  echo "Preparing the VirusFriends viral refseq database"
  local sequences="$VirusFriends_dbs/$1"
  printf "" > $sequences
  for i in 1 2
  do
    (set -x; $wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.$i.1.genomic.fna.gz" -O -  \
            | gunzip -d -c >> $sequences)
  done
  makeblastdb -title $1       \
              -in $sequences     \
              -out $sequences  \
              -dbtype 'nucl'  \
              -parse_seqids
  reset_wd
  return 0
}

function setup_viral_refseq_database()
{
  if [ $TESTONLY == 1 ]
    then echo "Making the VirusFriends viral refseq database"
    return
  fi
  virus_refseq="virus_refeseq_genomes"
  prepare_viral_refseq_database $virus_refseq
  return
}
