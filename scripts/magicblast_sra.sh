
#!/bin/bash
while read p; do
	echo "Processing SRA run $p."
	magicblast -sra $p -num_threads 6 -outfmt sam -out sam_output/$p.sam -no_query_id_trim  -splice F -no_unaligned  -db /data/RefSeq/viral.genomic.fna;
done <$1
