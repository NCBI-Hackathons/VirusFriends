#!/bin/bash
#-------------------------------------------------------------------------------
#  \file blast_setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \version 0.0.2
#  \description
#-------------------------------------------------------------------------------

function setup_blast()
{
  ftp_path="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/"
  if isInPath makeprofiledb
    then
      makeprofiledb=$(which makeprofiledb)
      echo "Found makeprofiledb: $makeprofiledb"
      return
  fi
  if [ $TESTONLY == 1 ]
    then echo "TEST: NCBI blast+ ($ftp_path) will be installed"
  fi

  if [ $INSTALL == 1 ]
    then
      echo "Installing NCBI blast+";
      cd $VirusFriends_tools
      $wget "$ftp_path/ncbi-blast-*-x64-linux.tar.gz" -O - | tar xvf -
      # bit of a hack to find the path name because blast includes the version number
      P=$(find . -name blastn | sed -e 's/blastn$//; s/^\.\///')
      expand_newpath "$PWD/$P"
  fi
  cd $BASEDIR
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

  if [ $TESTONLY == 1 ]
    then echo "TEST: MagicBlast ($ftp_path) will be installed"
    return
  fi

  echo "Installing magicblast"
  cd $VirusFriends_tools
#  wget "$ftp_path/ncbi-magicblast-1.3.0-x64-linux.tar.gz" -O - | tar xvf -
#  P=$(find . -name magicblast | sed -e 's/magicblast$//; s/^\.\///')
#  expand_newpath "$PWD/$P"
  cd $BASEDIR
}
