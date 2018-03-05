#!/bin/bash
#-------------------------------------------------------------------------------
#  \file spades_setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \version 0.0.2
#  \description
#-------------------------------------------------------------------------------

function install_spades()
{
  if [ $TESTONLY == 1 ]
    then
      echo "SPAdes will be installed ($1)"
      return
  fi
  local spades_dir="$VirusFriends_tools/SPAdes"
  mkdir -p $spades_dir
  echo "Installing SPAdes"
  $wget $1 -O - |  tar -C $spades_dir -xvzf -
  expand_newpath "$spades_dir/bin"
  cd $VirusFriends
}

function setup_spades()
{
  local ftp_path="http://cab.spbu.ru/files/release3.11.1/SPAdes-3.11.1-Linux.tar.gz"

  if isInPath 'spades'
    then
      echo "Found spades: $(which spades)"
      return
  fi
  install_spades $ftp_path
  return
}
