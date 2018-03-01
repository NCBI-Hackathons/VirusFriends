#!/bin/bash
#-------------------------------------------------------------------------------
#  \file blast_setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \version 0.0.2
#  \description
#-------------------------------------------------------------------------------

function install_blast()
{
  if [ $TESTONLY == 1 ]
    then echo "TEST: NCBI blast+ ($1) will be installed"
    return
  fi
  echo "Installing NCBI blast+";
  #cd $VirusFriends_tools
  #$wget "$1/ncbi-blast-*-x64-linux.tar.gz" -O - | tar xvf -
  ## bit of a hack to find the path name because blast includes the version number
  #P=$(find . -name blastn | sed -e 's/blastn$//; s/^\.\///')
  #expand_newpath "$PWD/$P"
}


function setup_blast()
{
  ftp_path="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/"
  if isInPath makeprofiledb
    then
      makeprofiledb=$(which makeprofiledb)
      echo "Found makeprofiledb: $makeprofiledb"
      return
  fi
  install_blast $ftp_path
  cd $BASEDIR
}

function install_magicblast()
{
  if [ $TESTONLY == 1 ]
      then echo "TEST: MagicBlast ($1) will be installed"
      return
  fi
  echo "Installing magicblast"
  cd $VirusFriends_tools
#  wget "$1/ncbi-magicblast-1.3.0-x64-linux.tar.gz" -O - | tar xvf -
#  P=$(find . -name magicblast | sed -e 's/magicblast$//; s/^\.\///')
#  expand_newpath "$PWD/$P"
}

function setup_magicblast()
{
  ftp_path="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST"
  if isInPath magicblast
    then
      magicblast=$(which magicblast)
      echo "Found magicblast: $magicblast"
      return
  fi
  install_magicblast $ftp_path
  cd $BASEDIR
}
