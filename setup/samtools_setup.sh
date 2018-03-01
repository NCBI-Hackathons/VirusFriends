#!/bin/bash
#-------------------------------------------------------------------------------
#  \file setup_samtools.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \version 0.0.2
#  \description
#-------------------------------------------------------------------------------
function get_samtool_version()
{
  samtools_version=$(echo $1 --version | grep samtools | cut -f ' ' -f2)
  samtools_maj=$(echo $version | cut -d. -f1)
  samtools_min=$(echo $version | cut -d. -f2)
}

function do_install_samtools()
{
  if [ $samtools_maj -le $MIN_SAMTOOLS_MAJOR]
    then
      [[ $samtools_min -lt $MIN_SAMTOOLS_MINOR ]] && return
    else
      return
  fi
}

function install_samtools()
{
  echo "Installing SAMtools"
  cd $VirusFriends_tools
  $wget  $1 -O - | tar  vxjf -
  cd samtools-1.7
  ./configure --prefix=$VirusFriends_tools/samtools-1.7/
  make
  make install
  cd ..
  local P=$(find . -name samtools | sed -e 's/samtools$//; s/^\.\///')
  expand_newpath "$PWD/$P"
  echo "Installed SAMtools in $PWD/$P"
}

function setup_samtools()
{
  local MIN_SAMTOOLS_MAJOR=1
  local MIN_SAMTOOLS_MINOR=7
  local ftp_path="https://github.com/samtools/samtools/releases/download/1.7/samtools-1.7.tar.bz2"
  local samtools_in_path=false

  if isInPath samtools
    then
      samtools=$(which samtools)
      get_samtool_version $samtools
      echo "Found samtools $samtools_version"
      samtools_in_path=true
  fi

  if [ $TESTONLY == 1 ]
    then
      if [ "$samtools_in_path" = true]
        then
          if do_install_samtools
            then
              echo "TEST: SAMTools v.1.7 will be installed ($ftp_path)"
              return
          fi
        else
          echo "TEST: SAMTools v.1.7 will be installed ($ftp_path)"
          return
      fi
  fi

  if [ "$samtools_in_path" = true ]
    then
      if do_install_samtools
        then
          install_samtools $ftp_path
      fi
    else
      install_samtools $ftp_path
  fi
  cd $BASEDIR
}
