#!/bin/bash
#  setup.sh
#
#  Copyright 2017 The University of Sydney
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0

esearch=$(which esearch)
efetch=$(which efetch)
xtract=$(which xtract)
makeprofiledb=$(which makeprofiledb)
endovir_pssms='endovir.pn'


export ENDOVIR=$(pwd)
endovir_dbs="$ENDOVIR/work/analysis/dbs"
endovir_tools="$ENDOVIR/tools"
mkdir -p $endovir_tools
mkdir -p $endovir_dbs

function setup_magicblast()
{
  echo " wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/ncbi-magicblast-1.3.0-x64-linux.tar.gz -P $endovir_tools -0 magicblast.tar.gz"
  exit 0
  wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/ncbi-magicblast-1.3.0-x64-linux.tar.gz -P $endovir_tools -0 "magicblast.tar.gz"
  tar  -C magicblast -xvf "$endovir_tools/magicblast.tar.gz"
  export PATH=$PATH:$endovir_tools/magicblast/bin
}

function make_endovir_cdd()
{

  echo "" > "$endovir_dbs/$endovir_pssms"
  local qry="txid10239[Organism:exp] NOT (predicted OR putative)"
  for i in $($esearch -db  cdd -query "$qry"                      | \
             $efetch -format docsum                               | \
             $xtract -pattern DocumentSummary -element Accession  | \
             grep -v cl)
    do
      echo $i".smp" >> "$endovir_dbs/$endovir_pssms"
    done

  local cdd_ftp='ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz'
  wget $cdd_ftp -O - | tar -C "$endovir_dbs/" -xzvT "$endovir_dbs/$endovir_pssms"
  cd $endovir_dbs
  $makeprofiledb -title "endovir"                    \
                 -in "$endovir_dbs/$endovir_pssms"   \
                 -out "$endovir_dbs/endovir_cdd"     \
                 -threshold 9.82                     \
                 -scale 100                          \
                 -dbtype rps                         \
                 -index true
}

make_endovir_cdd
