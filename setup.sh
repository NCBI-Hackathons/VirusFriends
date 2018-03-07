#!/bin/bash
#-------------------------------------------------------------------------------
#  \file setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \description Install and setup dependencies for VirusFriends
#  \version 0.0.2
#-------------------------------------------------------------------------------
## VirusFriends equivalents of $HOME and $PATH
export VirusFriends=$PWD
VF_PATH=""

## VirusFriends database directories
VirusFriends_dbs="$VirusFriends/analysis/dbs"
mkdir -p $VirusFriends_dbs

## VirusFriends tools
VirusFriends_tools="$VirusFriends/tools"
mkdir -p $VirusFriends_tools

## Basic OS tools. Maybe a tad too paranoid
wget=$(which wget)
make=$(which make)

## Global variables for setup
cpus=$(cat /proc/cpuinfo | grep processor | wc -l)
((cpus--))

efetch_bin=$(which efetch)
esearch_bin=$(which esearch)
xtract_bin=$(which xtract)
makeblastdb_bin=$(which makeblastdb)
makeprofiledb_bin=$(which makeprofildb)

## Load libaries
source $VirusFriends/setup/edirect_setup.sh
source $VirusFriends/setup/python_setup.sh
source $VirusFriends/setup/blast_setup.sh
source $VirusFriends/setup/samtools_setup.sh
source $VirusFriends/setup/spades_setup.sh
source $VirusFriends/setup/sratools_setup.sh
source $VirusFriends/setup/database_setup.sh

## essential functions
function isInPath()
{
 [[ ! -z $(which $1) ]] && return
}

# $1: path
function expand_vfpath()
{
  VF_PATH=$VF_PATH:$1
}
function reset_wd()
{
  cd $VirusFriends
}
function finish_up()
{
  if [ ! -z $VF_PATH ]; then
    VF_PATH=$(echo $VF_PATH | sed -e 's/^://')
    echo "You need to append $VF_PATH to your PATH environment variable."
    echo "I recommend doing this by adding the following line to ~/.bashrc"
    echo -e "\texport PATH=\$PATH:$VF_PATH"
    echo "but you may also want to add this to a different location so I didn't set it to you"
  fi
}

# $1 address $2 install_dir $3 compression: gzip|bzip
function wget_tool()
{
  local tar_cmd="tar -C $2 --strip-components=1 "
  if [[ "$3" == "gzip" ]]
    then
      tar_cmd+="-xz"
  fi

  if [[ "$3" == "bzip" ]]
    then
      tar_cmd+="-xj"
  fi
  tar_cmd+="vf -"
  (set -x; $wget $1 -O - | $tar_cmd)
}

function usage()
{
  echo "
 `basename $0` [-LV]
-L: List the software that will be installed. No changes will be made.
-I: Install the software

This installer will test for several pieces of software in your path and optionally install those that are missing.

If you provide the -L option, it will just list the software that will be installed.

If you provide the -I option, it will download appropriate software and install it. The default installation
directory is $VirusFriends_tools, but you can edit this install script to change that if you would prefer.

Databases will also be installed in $VirusFriends_dbs.
"
}

TESTONLY=0
INSTALL=0

if [ "$1" == "-L" ]; then
  TESTONLY=1;
  echo "Only listing software to be installed"
elif [ "$1" == "-I" ]; then
  INSTALL=1;
  echo "Installing software"
else
  usage
  exit 0
fi


echo "Will use $cpus CPU(s) for setup where possible"
## Go/no go poll
# Installing Python is a major PITA, can't get it to work properly.
#export PYTHONPATH=""
#export PYTHONHOME=""
#setup_python
setup_edirect
#setup_blast
#setup_magicblast
#setup_spades
#setup_sratools
#setup_samtools
setup_cdd_database
#setup_viral_refseq_database


if [ $TESTONLY == 1 ]
  then
    echo "VirusFriends test finished"
fi
finish_up
