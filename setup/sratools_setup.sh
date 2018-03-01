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

  echo "Installing SRAtoolkit"
  local sradir="$VirusFriends_tools/sratools"
  mkdir -p "$sradir"
  wget $1 -O - | tar -C $sradir --strip-components=1 -zxvf -
  P=$(find . -name vdb_dump | sed -e 's/sratools$//; s/^\.\///')
  NEWPATH=$NEWPATH:$PWD/$P
}


function setup_sratools()
{
  local ftp_path="https://github.com/ncbi/sra-tools/archive/2.8.2-5.tar.gz"
  if isInPath 'vdb_dump'
    then
      echo "Found vdb_dump, assuming working version of SRAtools: $(which vdb_dump)"
      return
  fi
  echo "TESTING MODE uncomment spades install cmd"
  install_sratools $ftp_path
  cd $BASEDIR

  if [ -z $sratools ]; then
          if [ $TESTONLY == 1 ]; then echo "SRA Toolkit (https://github.com/ncbi/sra-tools/archive/2.8.2-5.tar.gz) will be installed"; fi
          if [ $INSTALL == 1 ]; then

                  cd $BASEDIR
          fi
  fi
}
