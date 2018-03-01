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
  local esearch='esearch'
  local efetch='efetch'
  local xtract='xtract  '
  local SUCCESS=0

  printf "    $esearch: "
  if isInPath $esearch
    then
      printf "$(which $esearch)\n"
    else
      printf "None\n"
      SUCCESS=1
  fi
  printf "    $efetch: "
  if isInPath $efetch
    then
      printf "$(which efetch)\n"
    else
      printf "None\n"
      SUCCESS=1
  fi
  printf "    $xtract: "
  if isInPath $xtract
    then
      printf "$(which $xtract)\n"
    else
      echo "None"
      SUCCESS=1
  fi
  return $SUCCESS
}

function install_edirect()
{
  if [ $TESTONLY == 1 ]
    then
      echo "TEST: EDirect will be installed"
      return
  fi
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
      return
  fi
  install_edirect
  cd $BASEDIR
}
