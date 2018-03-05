#!/bin/bash
#-------------------------------------------------------------------------------
#  \file sratools_setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \version 0.0.2
#  \description
#-------------------------------------------------------------------------------

function install_sratools()
{
  if [ $TESTONLY == 1 ]
    then
      echo "SRATools will be installed ($1)"
      return
  fi
  echo "Installing SRAtoolkit ($1)"
  local sradir="$VirusFriends_tools/sratools"
  mkdir -p "$sradir"
  wget $1 -O - | tar -C $sradir --strip-components=1 -zxvf -
  expand_newpath "$sradir/bin/"
  cd $VirusFriends
}

function setup_sratools()
{
  vdbdump='vdb-dump'
  if isInPath $vdbdump
    then
      echo "Found $vdbdump, assuming working version of SRAtools: $(which $vdbdump)"
      return
  fi
  local ftp_path="https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2/sratoolkit.2.8.2-ubuntu64.tar.gz"
  install_sratools $ftp_path
  return
}
