#!/bin/bash
#-------------------------------------------------------------------------------
#  \file edirect_setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \version 0.0.2
#  \description
#-------------------------------------------------------------------------------
function has_edirect()
{
  local SUCCESS=0
  printf "    esearch: "
  if isInPath esearch
    then
      esearch=$(which esearch)
      printf "$esearch\n"
    else
      printf "None\n"
      SUCCESS=1
  fi
  printf "    efetch: "
  if isInPath efetch
    then
      efetch=$(which efetch)
      printf "$efetch\n"
    else
      printf "None\n"
      SUCCESS=1
  fi
  printf "    xtract: "
  if isInPath xtract
    then
      xtract=$(which xtract)
      echo "$xtract"
    else
      echo "None"
      SUCCESS=1
  fi
  return $SUCCESS
}

function install_edirect()
{
  echo "INSTALLING edirect in $VirusFriends_tools/edirect"
  cd $VirusFriends_tools
  ftp_path="ftp.ncbi.nlm.nih.gov//entrez/entrezdirect/edirect.tar.gz"
  $wget $ftp_path -O - | tar xf -
  ./edirect/setup.sh
  expand_newpath $PWD
}

function setup_edirect()
{
  echo "Checking for EDirect: NCBI edirect (https://www.ncbi.nlm.nih.gov/books/NBK179288/)"
  if has_edirect
    then
      echo "Found EDirect"
    else
      if [ $TESTONLY == 1 ]
        then
          echo "TEST: EDirect will be installed"
      fi
  fi
  if [ $INSTALL == 1 ]
    then
      install_edirect
  fi
  cd $BASEDIR
}
