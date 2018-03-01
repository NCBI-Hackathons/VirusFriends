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

}


function setup_sratools()
{
  local ftp_path="https://github.com/ncbi/sra-tools/archive/2.8.2-5.tar.gz"

  if isInPath 'vdb_dump'
    then
      echo "Found spades: $(which spades)"
      return
  fi
  if [ $TESTONLY == 1 ]
    then
      echo "SPAdes will be installed ($ftp_path)"
      return
  fi
  install_spades $ftp_path
  cd $BASEDIR

  sratools=$(which vdb_dump)
  if [ -z $sratools ]; then
          if [ $TESTONLY == 1 ]; then echo "SRA Toolkit (https://github.com/ncbi/sra-tools/archive/2.8.2-5.tar.gz) will be installed"; fi
          if [ $INSTALL == 1 ]; then
                  echo "Installing SRAtoolkit"
                  cd $VirusFriends_tools
                  wget https://github.com/ncbi/sra-tools/archive/2.8.2-5.tar.gz -O sratoolkit.tar.gz
                  tar  -xvzf sratoolkit.tar.gz
                  rm -f sratoolkit.tar.gz
                  P=$(find . -name vdb_dump | sed -e 's/sratools$//; s/^\.\///')
                  NEWPATH=$NEWPATH:$PWD/$P
                  cd $BASEDIR
          fi
  fi
}
