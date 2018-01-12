#!/bin/bash


if [ ! -n "$1" ] || [ ! -n "$2" ]; then
	echo "Usage: `basename $0` <list of SRA IDs> <magic blast database>"
	exit $E_BADARGS
fi



while read p; do
	echo "Processing SRA run $p."
	magicblast -sra $p -num_threads 6 -outfmt sam -out sam_output/$p.sam -no_query_id_trim  -splice F -no_unaligned  -db $2;
done <$1
