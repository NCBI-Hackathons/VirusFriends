#!/usr/bin/bash

# convert

samtools view -bS $1 | samtools sort > $1.bam

# depth -- this calculates relative coverage (where coverage is defined as more than 2 reads per base) over the length of the assembly

# samtools depth big.bam > big.bam.depth

samtools depth $1.bam > $1.bam.depth

# awk '{print $1}' big.bam.depth | sort -u > big.bam.accessions

awk '{print $1}' $1.bam.depth | sort -u > $1.bam.accessions

## for i in `cat big.bam.accessions`; do echo -n $i " "; awk -v i="$i" '{if ($1 == 'i') print $3}' big.bam.depth | sort | uniq -c | awk '{if ($2 < 3) print $0}' | awk '{sum += $1} END {printf sum" "}'; awk -v i="$i" '{if ($1 == 'i') print $3}' big.bam.depth | sort | uniq -c | awk '{if ($2 > 3) print $0}' | awk '{sum += $1} END {print sum}'; done

for i in `cat $1.bam.accessions`; do echo -n $i " "; awk -v i="$i" '{if ($1 == 'i') print $3}' $1.bam.depth | sort | uniq -c | awk '{if ($2 < 3) print $0}' | awk '{sum += $1} END {printf sum" "}'; awk -v i="$i" '{if ($1 == 'i') print $3}' $1.bam.depth | sort | uniq -c | awk '{if ($2 > 3) print $0}' | awk '{sum += $1} END {print sum}'; done

##

# clean up what you dont want 

