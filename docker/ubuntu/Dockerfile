#-------------------------------------------------------------------------------
#  \file python_setup.sh
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \version 0.0.1
#  \description Docker image for testing VirusFriends on Ubuntu
#-------------------------------------------------------------------------------

FROM ubuntu:latest

RUN apt-get -q update &&                    \
    apt-get install -y build-essential      \
                       libncurses5-dev      \
                       zlib1g-dev           \
                       libbz2-dev           \
                       liblzma-dev          \
                       libcurl4-gnutls-dev  \
                       git                  \
                       wget                 \
                       libssl-dev           \
                       bzip2

RUN adduser --quiet --disabled-password --gecos '' virusfriend
RUN su - virusfriend -c "cd /home/virusfriend && \
                         git clone https://github.com/NCBI-Hackathons/VirusFriends && \
                         cd VirusFriends && \
                         git checkout -b testing && \
                         git pull  origin testing"
