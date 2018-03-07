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
  echo "Installing NCBI blast+ ($1)"
  local blast_dir="$VirusFriends_tools/blast"
  mkdir -p $blast_dir
  wget_tool $1 $blast_dir "gzip"
  makeblastdb_bin="$blast_dir/bin/makeblastdb"
  makeprofiledb_bin="$blast_dir/bin/makeprofiledb"
  expand_vfpath "$blast_dir/bin"
  cd $VirusFriends
}

function setup_blast()
{
  if isInPath makeprofiledb
    then
      makeprofiledb=$(which makeprofiledb)
      echo "Found makeprofiledb: $makeprofiledb. Assuming installed BLAST"
      return
  fi
  local ftp_path="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/"
  local version="ncbi-blast-*-x64-linux.tar.gz"
  install_blast "$ftp_path/$version"
  return
}

function install_magicblast()
{
  if [ $TESTONLY == 1 ]
      then echo "TEST: MagicBlast ($1) will be installed"
      return
  fi
  echo "Installing magicblast ($1)"
  cd $VirusFriends_tools
  local mblast_dir="$VirusFriends_tools/magicblast"
  mkdir -p $mblast_dir
  wget_tool $1 $mblast_dir "gzip"
  expand_vfpath "$mblast_dir/bin"
  cd $VirusFriends
}

function setup_magicblast()
{
  if isInPath magicblast
    then
      magicblast=$(which magicblast)
      echo "Found magicblast: $magicblast"
      return
  fi
  local ftp_path="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST"
  local version="ncbi-magicblast-1.3.0-x64-linux.tar.gz"
  install_magicblast "$ftp_path/$version"
  return
}
