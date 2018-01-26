import argparse
import sys
import pysam

class Sorter:
    def __init__(self):
        self.MIN_MATCHED_BASES = 50
        self.WEAK_MATCH_THRESHOLD=0.8
        self.STRONG_MATCH_THRESHOLD=0.7
        self.STRONG_ORGANISM_MIN_COVERAGE=0.8
        

    def sort_matches(self, samfile, outdir, MIN_MATCHED_BASES = 50, WEAK_MATCH_THRESHOLD=0.8, STRONG_MATCH_THRESHOLD=0.7, STRONG_ORGANISM_MIN_COVERAGE=0.8, log=True):
        print("in sort_matches, samfile is %s and outdir is: %s" % (samfile, outdir))

        if not outdir.endswith('/'):
            outdir = outdir + '/'

        new_name = samfile.split('.')[0].split('/')[-1]

        if samfile.endswith('.sam'):
            readtype = 'r'
        elif samfile.endswith('.bam'):
            readtype = 'rb'
        else:
            sys.stderr.write('samfile {} does not end with .sam or .bam, trying as samfile...\n'.format(samfile))
            readtype = 'r'
        try:
            samfile = pysam.AlignmentFile(samfile, readtype)
        except Exception as e:
            sys.stderr.write(
            'samfile {} could not be opened by pysam, check that it is a BAM/SAM file. Error:\n{}\n'.format(samfile, e))
            sys.exit(1)

        # Get a dict of genome lengths from the header
        genome_lengths = {}
        for l, r in zip(samfile.lengths, samfile.references):
            genome_lengths[r] = l

        # Check each organism for coverage
        organism_coverage = {}
        for read in samfile.fetch():
            genome_name = read.reference_name
            if genome_name in organism_coverage:
                continue

            # Process one genome
            base_depth = []
            for p in samfile.pileup(contig=genome_name):
                for pilups in p.pileups:
                    if pilups.query_position:
                        # Expand array while insert pos is out of list bounds
                        if p.reference_pos >= len(base_depth):
                            while p.reference_pos >= len(base_depth):
                                base_depth.append(0)
                        base_depth[p.reference_pos] += 1

            bins_covered = len([x for x in base_depth if x > 0])
            organism_coverage[genome_name] = bins_covered / genome_lengths[genome_name]

        # Create a list of genome names with coverage below MIN_PERCENT_COVERAGE
        weak_organisms = set()
        for k,v in organism_coverage.items():
            if v < STRONG_ORGANISM_MIN_COVERAGE:
                weak_organisms.add(k)

        strong_reads = []
        weak_reads = []
        for read in samfile.fetch():
            #print ("found a read: %s" % read)
            x, y = read.get_cigar_stats()
            matched_bases = x[0]
            if matched_bases < MIN_MATCHED_BASES:
                #if log:
                #print('low match length: {}\n'.format(read.reference_name))
                continue
            if read.reference_name in weak_organisms:
                weak_reads.append(read)
                continue
            total_bases = int(sum(x))
            percent_match = (matched_bases / float(total_bases))
            #print(percent_match)
            if percent_match <= WEAK_MATCH_THRESHOLD:
                #if log:
                #    print('weak match: {}\n'.format(read.reference_name))
                weak_reads.append(read)
            if percent_match >= STRONG_MATCH_THRESHOLD:
                #if log:
                #print('strong match: {}\n'.format(read.reference_name))
                strong_reads.append(read)

        #write strong reads to new file:
        with open(outdir + 'strong_' + new_name + '.fasta', 'w') as outfile:
            for read in strong_reads:
                refname = read.query_name
                dna = read.get_reference_sequence()
                outfile.write('>{}\n{}\n'.format(refname, dna))

        #write fasta file
        with open(outdir + 'weak_' + new_name + '.fasta', 'w') as outfile:
            for read in weak_reads:
                refname = read.query_name
                dna = read.get_reference_sequence()
                outfile.write('>{}\n{}\n'.format(refname, dna))
