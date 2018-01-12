# Testing Virus Friends

To test this software, we have provided the crAssphage sequence from [Dutilh _et al_](https://www.nature.com/articles/ncomms5498), and a [small list of SRA IDs](sra_ids.txt), some of which have the sequence. The SRA IDs are from BioProject [PRJNA275568](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA275568/) where they characterized the onset of islet autoimmunity by sequencing stool viromes.

## Magic Blast

Once you have [installed](../INSTALL.md) magic blast and the RefSeq viral database, you can test magic blast using this command.

```
bash VirusFriends/scripts/magicblast_sra.sh VirusFriends/test/sra_ids.txt viral.genomic.fna
```

It should create lots of [sam](https://samtools.github.io/) files for you!

