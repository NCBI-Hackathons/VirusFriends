#!/bin/bash
#  setup.sh
#
#  Copyright 2017 The University of Sydney
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Author: Robert Edwards <raedwards@gmail.com>
#  Author: Bhavya Papudeshi<npbhavya13@gmail.com>
#  Description:
#   Install some dependencies for VirusFriends
#
#  Version: 0

export VirusFriends=$PWD
VirusFriends_dbs="$VirusFriends/analysis/dbs"
VirusFriends_tools="$VirusFriends/tools"
VirusFriends_pssms='VirusFriends.pn'
BASEDIR=$PWD

TESTONLY=0
INSTALL=0
if [ "$1" == "-L" ]; then 
	TESTONLY=1; 
	echo "Only listing software to be installed"
elif [ "$1" == "-I" ]; then 
	INSTALL=1;
	echo "Installing software"
else
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
	exit 0 
fi

mkdir -p $VirusFriends_tools
mkdir -p $VirusFriends_dbs

NEWPATH=""

function install_edirect()
{
	## check for edirect
	esearch=$(which esearch)
	efetch=$(which efetch)
	xtract=$(which xtract)
	if [ -z $esearch ] || [ -z $efetch ] || [ -z $xtract ]; then
		## edirect
		if [ $TESTONLY == 1 ]; then echo "NCBI edirect (https://www.ncbi.nlm.nih.gov/books/NBK179288/) will be installed"; fi
		if [ $INSTALL == 1 ]; then
			echo "INSTALLING edirect in $endovir_tools/edirect"
			cd $VirusFriends_tools
			perl -MNet::FTP -e \
			    '$ftp = new Net::FTP("ftp.ncbi.nlm.nih.gov", Passive => 1);
			     $ftp->login; $ftp->binary;
			     $ftp->get("/entrez/entrezdirect/edirect.tar.gz");'
			     gunzip -c edirect.tar.gz | tar xf -
			     rm -f edirect.tar.gz
			     ./edirect/setup.sh
			NEWPATH=$NEWPATH:$PWD
			cd $BASEDIR
		fi
	fi
}

function install_blast()
{
	makeprofiledb=$(which makeprofiledb)
	if [ -z $makeprofiledb ]; then
		## blast+
		if [ $TESTONLY == 1 ]; then echo "NCBI blast+ (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/) will be installed"; fi
		if [ $INSTALL == 1 ]; then
			echo "Installing NCBI blast+";
			cd $VirusFriends_tools
			wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-*-x64-linux.tar.gz -O blast.tgz
			tar xf blast.tgz
			rm -f blast.tgz
			# bit of a hack to find the path name because blast includes the version number
			P=$(find . -name blastn | sed -e 's/blastn$//; s/^\.\///')
			NEWPATH=$NEWPATH:$PWD/$P
			cd $BASEDIR
		fi
	fi
}

function setup_magicblast()
{
	magicblast=$(which magicblast)
	if [ -z $magicblast ]; then
		if [ $TESTONLY == 1 ]; then echo "MagicBlast (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST) will be installed"; fi
		if [ $INSTALL == 1 ]; then
			echo "Installing magicblast"
			cd $VirusFriends_tools
			wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/ncbi-magicblast-1.3.0-x64-linux.tar.gz -O magicblast.tar.gz
			tar  -xvf magicblast.tar.gz
			rm -f magicblast.tar.gz
			P=$(find . -name magicblast | sed -e 's/magicblast$//; s/^\.\///')
			NEWPATH=$NEWPATH:$PWD/$P
			cd $BASEDIR
		fi
	fi
}

function python3_check()
{
        python=$(python3 --version)
	python_version=$( echo $python | cut -d ' ' -f2 )
        if [ "$python_version" != 3.5.5 ]; then
                if [ $TESTONLY == 1 ]; then echo "Installing Python v3.5.5(https://www.python.org/ftp/python/3.5.5/Python-3.5.5.tgz) will be installed"; fi
                if [ $INSTALL == 1 ]; then
                        echo "Installing python3"
                        cd $VirusFriends_tools
                        wget https://www.python.org/ftp/python/3.5.5/Python-3.5.5.tgz -O python.tar.gz
                        tar  -xvf python.tar.gz
                        rm -f python.tar.gz
			cd Python-3.5.5
			./configure --prefix=$VirusFriends_tools/Python-3.5.5/
			make && make install
			#checking pip3 install
			pip3=$(which pip3)
			if [ -z $pip3 ]; then
			if [ $INSTALL == 1 ]; then
				wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py -O - | python - --user
				fi
			fi
			#exiting directory and adding the paths for python
			cd ..
			export PATH=$VirusFriends_tools/Python-3.5.5/bin:$PATH
			export PYTHONPATH=$VirusFriends_tools/Python-3.5.5:$PYTHONPATH
                        #checking for pysam install, making an assumption you have root access on the machine. Code needs to be fixed for non-root install
			pip3 install pysam --user
			pip3 install biopython --user
			cd $BASEDIR
                fi
        fi
}

function setup_samtools()
{
	samtools_v=$(samtools --version)
	version=$( echo $samtools_v | cut -d ' ' -f2 )
	if [ -z $version != 1.7 ]; then
                if [ $TESTONLY == 1 ]; then echo "SAMtools (https://github.com/samtools/samtools/releases/download/1.7/samtools-1.7.tar.bz2) will be installed"; fi
                if [ $INSTALL == 1 ]; then
                        echo "Installing SAMtools"
                        cd $VirusFriends_tools
                        wget  https://github.com/samtools/samtools/releases/download/1.7/samtools-1.7.tar.bz2 -O samtools.tar.bz2
                        tar  -vxjf samtools.tar.bz2
                        rm -f samtools.tar.bz2
			cd samtools-1.7
			./configure --prefix=$VirusFriends_tools/samtools-1.7/
			make && make install
			cd ..
			P=$(find . -name samtools | sed -e 's/samtools$//; s/^\.\///')
                        NEWPATH=$NEWPATH:$PWD/$P
                        cd $BASEDIR
                fi
        fi
}

function setup_spades()
{
        spades=$(which spades)
        if [ -z $spades ]; then
                if [ $TESTONLY == 1 ]; then echo "SPAdes (http://cab.spbu.ru/files/release3.11.1/SPAdes-3.11.1-Linux.tar.gz) will be installed"; fi
                if [ $INSTALL == 1 ]; then
                        echo "Installing SPAdes"
                        cd $VirusFriends_tools
                        wget  http://cab.spbu.ru/files/release3.11.1/SPAdes-3.11.1-Linux.tar.gz -O spades.tar.gz
                        tar  -xvzf spades.tar.gz 
                        rm -f spades.tar.gz
                        P=$(find . -name spades.py | sed -e 's/spades$//; s/^\.\///')
                        NEWPATH=$NEWPATH:$PWD/$P
                        cd $BASEDIR
                fi
        fi
}

function setup_sratools()
{
        sratools=$(which vdb_dump)
        if [ -z $sratools ]; then
                if [ $TESTONLY == 1 ]; then echo "SRA Toolkit (https://github.com/ncbi/sra-tools/archive/2.8.2-5.tar.gz) will be installed"; fi
                if [ $INSTALL == 1 ]; then
                        echo "Installing SRAtoolkit"
                        cd $VirusFriends_tools
                        wget https://github.com/ncbi/sra-tools/archive/2.8.2-5.tar.gz -O sratoolkit.tar.gz
                        tar  -xvzf sratoolkit.tar.gz
                        rm -f sratoolkit.tar.gz
                        P=$(find . -name vdb_dump | sed -e 's/sratools$//; s/^\.\///')
                        NEWPATH=$NEWPATH:$PWD/$P
                        cd $BASEDIR
                fi
        fi
}


function make_endovir_cdd()
{

	if [ $TESTONLY == 1 ]; then echo "Making the VirusFriends CDD libraries"; fi
	if [ $INSTALL == 1 ]; then 
		echo "Making the VirusFriends CDD libraries";
		echo "" > "$VirusFriends_dbs/$VirusFriends_pssms"
		local qry="txid10239[Organism:exp] NOT (predicted OR putative)"
		for i in $($esearch -db  cdd -query "$qry"                | \
		     $efetch -format docsum                               | \
		     $xtract -pattern DocumentSummary -element Accession  | \
		     grep -v cl);
		do
	     		echo $i".smp" >> "$VirusFriends_dbs/$VirusFriends_pssms"
    		done

		  local cdd_ftp='ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz'
		  wget $cdd_ftp -O - | tar -C "$VirusFriends_dbs/" -xzvT "$VirusFriends_dbs/$VirusFriends_pssms"
		  cd $VirusFriends_dbs
		  $makeprofiledb -title "endovir"                    \
				 -in "$VirusFriends_dbs/$VirusFriends_pssms"   \
				 -out "$VirusFriends_dbs/endovir_cdd"     \
				 -threshold 9.82                     \
				 -scale 100                          \
				 -dbtype rps                         \
				 -index true
	fi
}

function make_viralrefseq_database()
{

        if [ $TESTONLY == 1 ]; then echo "Making the VirusFriends viral refseq database"; fi
        if [ $INSTALL == 1 ]; then
                echo "Making the VirusFriends viral refseq database";
		wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.1.genomic.fna.gz -O $VirusFriends_dbs/viral.genomic.fna.gz
                gunzip -d  $VirusFriends_dbs/viral.genomic.fna.gz
		makeblastdb -title viral.genomic.refseq.fna  -in $VirusFriends_dbs/viral.genomic.fna  \
				-out $VirusFriends_dbs/viral.genomic.refseq.fna -dbtype nucl -parse_seqids 
        fi
}


function finish_up()
{
	if [ ! -z $NEWPATH ]; then
		NEWPATH=$(echo $NEWPATH | sed -e 's/^://')
		echo "You need to append $NEWPATH to your PATH environment variable."
		echo "I recommend doing this by adding the following line to ~/.bashrc"
		echo -e "\texport PATH=\$PATH:$NEWPATH"
		echo "but you may also want to add this to a different location so I didn't set it to you"
		export PATH=$NEWPATH:$PATH
	fi
}

install_edirect
install_blast
setup_magicblast
setup_spades
setup_sratoolkit
setup_samtools
python3_check
make_endovir_cdd
make_viralrefseq_database
finish_up

