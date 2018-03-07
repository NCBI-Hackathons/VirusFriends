#!/bin/bash
#-------------------------------------------------------------------------------
#  \file python_setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \author Robert Edwards <raedwards@gmail.com>
#  \author Bhavya Papudeshi<npbhavya13@gmail.com>
#  \version 0.0.2
#  \description
#-------------------------------------------------------------------------------

function get_python_version()
{
  python_version=$($1 --version | cut -d ' ' -f2)
  python_version_maj=$(echo $python_version | cut -d. -f1)
  python_version_min=$(echo $python_version | cut -d. -f2)
  python_version_patch=$(echo $python_version | cut -d. -f3)
}

function hasRequiredVersionPython()
{
  PYTHON_MIN_MAJ=3
  PYTHON_MIN_MIN=5
  PYTHON_MIN_PATCH=5

  if [[ $python_version_maj -eq $PYTHON_MIN_MAJ ]]
    then
      if [[ $python_version_min -gt $PYTHON_MIN_MIN ]]
        then
          return
      elif [[ $python_version_min -eq $PYTHON_MIN_MIN ]]
        then
          [[ $python_version_patch -ge $PYTHON_MIN_PATCH ]]
          return
      else
        return
      fi
    else
      return
  fi
}

function install_python()
{
  if [ $TESTONLY == 1 ]
    then
      echo "TEST: Python v3.5.5 will be installed ($1)"
      return
  fi

  echo "Installing python 3.5.5 ($1)"
  local python_dir="$VirusFriends_tools/python"
  mkdir -p $python_dir
  wget $1 -O - | tar -C $python_dir --strip-components=1 -zxvf -
  cd $python_dir
  echo $PWD
  ./configure --prefix=$python_dir
  make -j$cpus && make install
  export PYTHONHOME="$python_dir/bin/"
  export PYTHONPATH="$python_dir/lib/python3.5/:$python_dir/lib/python3.5/site-packages/"
  #      PYTHONPATH=/home/virusfriend/VirusFriends/tools/python/lib/python3.5
  expand_vfpath $PYTHONHOME
  expand_vfpath $PYTHONPATH
  export PATH="$PATH:$python_dir/bin"
  echo "------------------------"
  echo $PYTHONHOME
  echo $PYTHONPATH
  echo "------------------------"
  expand_vfpath "$python_dir"
  local pip='pip3'
  $pip install --user pysam
  $pip install --user biopython
  cd $VirusFriends
  return 0
}

function setup_python()
{
  local python_ftp_path="https://www.python.org/ftp/python/3.5.5/Python-3.5.5.tgz"

  if isInPath 'python3'
    then
      python=$(which python3)
      get_python_version $python
      if hasRequiredVersionPython
        then
          echo "Found Python $python_version (Required: $PYTHON_MIN_MAJ.$PYTHON_MIN_MIN.$PYTHON_MIN_PATCH)"
          return
      fi
  fi
  install_python $python_ftp_path
  return
}
