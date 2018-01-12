#!/bin/bash
#  setup.sh
#
#  Copyright 2017 The University of Sydney
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Author: Robert Edwards <raedwards@gmail.com>
#  Description:
#   Install some dependencies for VirusFriends
#
#  Version: 0

export ENDOVIR=$PWD
endovir_dbs="$ENDOVIR/work/analysis/dbs"
endovir_tools="$ENDOVIR/tools"
endovir_pssms='endovir.pn'
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
directory is $endovir_tools, but you can edit this install script to change that if you would prefer.

Databases will also be installed in $endovir_dbs.
"
	exit 0 
fi

mkdir -p $endovir_tools
mkdir -p $endovir_dbs



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
			cd $endovir_tools
			mkdir edirect
			cd edirect
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
			cd $endovir_tools
			wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/LATEST/ncbi-blast-*-x64-linux.tar.gz -O blast.tgz
			tar xf blast.tgz
			rm -f blast.tgz
			# bit of a hack to find the path name because blast includes the version number
			P=$(find . -name blastn | sed -e 's/blastn$//; s/^\.\///')
			NEWPATH=$NEWPATH:$P
			cd $BASEDIR
		fi
	fi
}



function setup_magicblast()
{
	magicblast=$(which magicblast)
	if [ -z $magicblast ]; then
		if [ $TESTONLY == 1 ]; then echo "MagicBlast (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST) whill be installed"; fi
		if [ $INSTALL == 1 ]; then
			echo "Installing magicblast"
			cd $endovir_tools
			wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/ncbi-magicblast-1.3.0-x64-linux.tar.gz -O magicblast.tar.gz
			tar  -xvf magicblast.tar.gz
			rm -f magicblast.tar.gz
			P=$(find . -name magicblast | sed -e 's/magicblast$//; s/^\.\///')
			NEWPATH=$NEWPATH:$P
			cd $BASEDIR
		fi
	fi
}

function make_endovir_cdd()
{

	if [ $TESTONLY == 1 ]; then echo "Making the VirusFriends CDD libraries"; fi
	if [ $INSTALL == 1 ]; then 
		echo "Making the VirusFriends CDD libraries";
		echo "" > "$endovir_dbs/$endovir_pssms"
		local qry="txid10239[Organism:exp] NOT (predicted OR putative)"
		for i in $($esearch -db  cdd -query "$qry"                | \
		     $efetch -format docsum                               | \
		     $xtract -pattern DocumentSummary -element Accession  | \
		     grep -v cl);
		do
	     		echo $i".smp" >> "$endovir_dbs/$endovir_pssms"
    		done

		  local cdd_ftp='ftp://ftp.ncbi.nlm.nih.gov/pub/mmdb/cdd/cdd.tar.gz'
		  wget $cdd_ftp -O - | tar -C "$endovir_dbs/" -xzvT "$endovir_dbs/$endovir_pssms"
		  cd $endovir_dbs
		  $makeprofiledb -title "endovir"                    \
				 -in "$endovir_dbs/$endovir_pssms"   \
				 -out "$endovir_dbs/endovir_cdd"     \
				 -threshold 9.82                     \
				 -scale 100                          \
				 -dbtype rps                         \
				 -index true
	fi
}


function finish_up()
{
	if [ ! -z $NEWPATH ]; then
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
make_endovir_cdd
finish_up
