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

function hasRequiredVersion()
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
  cd $VirusFriends_tools
  wget $1 -O - | tar zxvf -
  cd Python-3.5.5
  ./configure --prefix=$VirusFriends_tools/Python-3.5.5/
  make
  make install

  local pip='pip3'
  if ! isInPath $pip
    then
      echo "Installing python $pip"
      wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py -O - | python - --user
  fi
  export PATH=$VirusFriends_tools/Python-3.5.5/bin:$PATH
  export PYTHONPATH=$VirusFriends_tools/Python-3.5.5:$PYTHONPATH
  pip_bin=$(which $pip)
  $pip_bin install pysam --user
  $pip_bin biopython --user
}

function setup_python()
{
  local python_ftp_path="https://www.python.org/ftp/python/3.5.5/Python-3.5.5.tgz"

  if isInPath "python3"
    then
      python=$(which python3)
      get_python_version $python
      if hasRequiredVersion
        then
          echo "Found Python $python_version"
          return
      fi
  fi
  echo "TESTING MODE uncomment python install cmd"
  #install_python $python_ftp_path
  cd $BASEDIR
}
