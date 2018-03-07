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
      esearch_bin=$(which $esearch)
      printf "$esearch_bin\n"
    else
      printf "None\n"
      SUCCESS=1
  fi
  printf "    $efetch: "
  if isInPath $efetch
    then
      efetch_bin=$(which efetch)
      printf "$efetch_bin\n"
    else
      printf "None\n"
      SUCCESS=1
  fi
  printf "    $xtract: "
  if isInPath $xtract
    then
      xtract_bin=$(which $xtract)
      printf "$xtract_bin\n"
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
  local edirect_dir="$VirusFriends_tools/edirect"
  mkdir -p $edirect_dir
  echo "INSTALLING edirect in $edirect_dir"
  perl -MNet::FTP -e \
    '$ftp = new Net::FTP("ftp.ncbi.nlm.nih.gov", Passive => 1);
     $ftp->login; $ftp->binary;
     $ftp->get("/entrez/entrezdirect/edirect.tar.gz");'
  tar -C "$edirect_dir" --strip-components=1 -xzf edirect.tar.gz
  rm edirect.tar.gz
  sh $edirect_dir/setup.sh
  expand_vfpath $edirect_dir
  reset_wd
  return 0
}

function setup_edirect()
{
  echo "Checking for EDirect: NCBI edirect (https://www.ncbi.nlm.nih.gov/books/NBK179288/)"
  if has_edirect
    then
      echo "Found EDirect"
      return
  fi
  local ftp_path="ftp.ncbi.nlm.nih.gov//entrez/entrezdirect/edirect.tar.gz"
  install_edirect $ftp_path
  return
}
