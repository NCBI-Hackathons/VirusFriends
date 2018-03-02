#!/bin/bash
#-------------------------------------------------------------------------------
#  \file database_setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#-------------------------------------------------------------------------------

function prepare_cdd_database()
{
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
  $wget $2 -O - | tar -C "$cdd_smp_dir/" -xzvT $1 -f -
  cd $cdd_smp_dir
  makeprofiledb -title endovir     \
                 -in $1            \
                 -out ../$cdd_db      \
                 -dbtype rps       \
                 -threshold 9.82   \
                 -scale 100        \
                 -index true
  cd $VirusFriends
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
  printf "" > $cdd_pssms  # reset pn file
  local cdd_ftp='ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz'
  [[ $(prepare_cdd_database $cdd_pssms $cdd_ftp) -eq 0 ]] && return
}

#function prepare_viral_refseq_database()
#{
  #part1="viral.1.1.genomic.fna.gz"
  #echo "Preapring the VirusFriends viral refseq database"

  #$wget $1 -O $VirusFriends_dbs/viral.genomic.fna.gz
                #gunzip -d  $VirusFriends_dbs/viral.genomic.fna.gz
    #makeblastdb -title viral.genomic.refseq.fna  -in $VirusFriends_dbs/viral.genomic.fna  \
        #-out $VirusFriends_dbs/viral.genomic.refseq.fna -dbtype nucl -parse_seqids
        #fi
#}

function setup_viral_refseq_database()
{
  if [ $TESTONLY == 1 ]
    then echo "Making the VirusFriends viral refseq database"
    return
  fi
  local ftp_base_path="ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/"
  [[ $(prepare_viral_refseq_database $ftp_path) -eq 0 ]] && return
}
