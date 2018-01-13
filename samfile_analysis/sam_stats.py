import argparse
import sys
import pysam
import math
import os
import subprocess


def sort_matches(samfile_name, outdir, MIN_MATCHED_BASES=50):
    new_name = samfile_name.split('.')[0].split('/')[-1]
    if not outdir.endswith('/'):
        outdir = outdir + '/'

    if samfile_name.endswith('.sam'):
        readtype = 'r'
    elif samfile_name.endswith('.bam'):
        readtype = 'rb'
    else:
        sys.stderr.write('samfile {} does not end with .sam or .bam, trying as samfile...\n'.format(samfile))
        readtype = 'r'
    try:
        samfile = pysam.AlignmentFile(samfile_name, readtype)
    except Exception as e:
        sys.stderr.write(
            'samfile {} could not be opened by pysam, check that it is a BAM/SAM file. Error:\n{}\n'.format(samfile, e))
        sys.exit(1)

    genome_lengths = {}
    for l, r in zip(samfile.lengths, samfile.references):
        genome_lengths[r] = l

    x = subprocess.Popen(['bash', 'depth_charger.sh', '{}'.format(samfile_name)], stdout=subprocess.PIPE)
    genome_coverage = {}
    x = x.communicate()[0].decode('utf-8')
    #print('output from depth_charger is: {}'.format(x))
    x = x.split('\n')
    for line in x:
        if len(line) < 1: continue
        line = line.split(' ')
        genome_coverage[line[0]] = float(line[3]) / genome_lengths[line[0]]
    #print(genome_coverage)
    print('conservation done')


    '''
    # Create pilup for each organism --- WORKS BUT VERY SLOW 
    organism_coverage = {}
    i = 0
    for column in samfile.pileup():
        # print('columnpos: {}\n'.format(column.reference_pos))
        if column.reference_name not in organism_coverage:
            organism_coverage[column.reference_name] = [0 for x in range(genome_lengths[column.reference_name])]
        for pileupread in column.pileups:
            organism_coverage[pileupread.alignment.reference_name][column.reference_pos] += 1

    for k, v in organism_coverage.items():
        percent_coverage = len([0 for x in v if x > 0]) / float(genome_lengths[k])

        organism_coverage[k] = percent_coverage
        print('{}: {}'.format(k, organism_coverage[k]))
    '''



    organism_match_bins = {}  # {organism: [[100% matches], [99% matches], ... [0% matches]], second_organism[[], [], .. []]}
    for read in samfile.fetch():
        x, y = read.get_cigar_stats()
        matched_bases = x[0]
        if matched_bases < MIN_MATCHED_BASES:
            # print('low match length, skipping: {}\n'.format(read.reference_name))
            continue

        organism_name = read.reference_name
        total_bases = int(sum(x))
        percent_match = (matched_bases / float(total_bases))

        if organism_name not in organism_match_bins:
            organism_match_bins[organism_name] = [[] for x in range(100)]
        bin = 100 - math.ceil(percent_match * 100)
        organism_match_bins[organism_name][bin].append(total_bases)

    # write .csv file
    with open(outdir + new_name + '.tsv', 'w') as outfile:
        outfile.write('Organism\t% Genome Covered\tTotal Matches\t95%+ Matches\tGenome Length\n')
        for k, v in sorted(organism_match_bins.items()):
            outfile.write('{}\t{}\t{}\t{}\t{}\n'.format(k, str(genome_coverage[k]), str(sum([len(x) for x in v])), str(sum([len(x) for x in v[:5]])), genome_lengths[k]))
            # This snippet will output the full bins:    '\t'.join([str(x) for x in v])   Matched Bases in each bin from 99+%  ->  0%


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reads a SAM or BAM file and appends a CSV file with information about the matched reads')
    parser.add_argument('-i', '--input', help='Name of the input .sam file to be read', required=True)
    parser.add_argument('-o', '--output',
                        help='Name of the DIRECTORY to write weakly mached reads (.fasta) and samfile stats (.tsv)',
                        required=True)
    parser.add_argument('-l', '--length', help='Ignore all matches shorter than -l base pairs, default is 50', type=int)

    parser.add_argument('-v', '--verbose', help='Output a log file of the initial input stats. NOT WORKING',
                        action='store_true')
    parser.add_argument('-s', '--stdout', help='If used, output the FASTA to standard output.', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    if not args.length:
        args.length = 50



    sort_matches(args.input, args.output, args.length)
    sys.exit(0)
