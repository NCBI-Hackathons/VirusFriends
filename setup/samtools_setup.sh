#!/bin/bash
#-------------------------------------------------------------------------------
#  \file setup_samtools.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \version 0.0.2
#  \description
#-------------------------------------------------------------------------------
function get_samtools_version()
{
  local version=$($1 --version | grep samtools| cut -d' ' -f2|cut -d'-' -f1)
  samtools_maj=$(echo $version | cut -d. -f1)
  samtools_min=$(echo $version | cut -d. -f2)
}
function hasRequiredVersionSamtools()
{
  local MIN_SAMTOOLS_MAJOR=1
  local MIN_SAMTOOLS_MINOR=7

  if [[ $samtools_maj -gt $MIN_SAMTOOLS_MAJOR ]]
    then
      return
    else
      if [[ $samtools_maj -eq $MIN_SAMTOOLS_MAJOR ]]
        then
          return
      else
        [[ $samtools_min -ge $MIN_SAMTOOLS_MINOR ]]
        return
      fi
  fi
}

function install_samtools()
{
  if [ $TESTONLY == 1 ]
    then
      echo "SRATools will be installed ($1)"
      return
  fi
  local samtools_dir="$VirusFriends_tools/samtools"
  local samtools_build_dir="$samtools_dir/build"
  echo "Installing SAMtools"
  mkdir -p "$samtools_build_dir"
  $wget  $1 -O - | tar  -C $samtools_build_dir --strip-components=1 -vxjf -
  cd $samtools_dir
  ./configure --prefix=$samtools_build_dir
  make -j$cpus && make install
  expand_newpath "$samtools_build_dir/bin"
  echo "Installed SAMtools in $samtools_build_dir/bin"
}

function setup_samtools()
{
  local ftp_path="https://github.com/samtools/samtools/releases/download/1.7/samtools-1.7.tar.bz2"
  local samtools='samtools'

  if isInPath $samtools
    then
      get_samtools_version $(which $samtools)
      if hasRequiredVersionSamtools
        then
          echo "Found $(eval $(which $samtools) --version | grep samtools)"
          return
      fi
  fi
 echo "TESTING MODE uncomment samtool install cmd"
 #install_samtools $ftp_path
 cd $VirusFriends
}
