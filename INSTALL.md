# Installing Virus Friends


## Dependencies

There are several dependencies that are required for Virus Friends:
- [Magic BLAST](https://boratyng.github.io/magicblast/)
  * You can download Magic BLAST from the [NCBI ftp site](https://goo.gl/oLzUvD)

- [Viral Refseq](https://www.ncbi.nlm.nih.gov/genome/viruses/)
  * You will need to download viral RefSeq. You can grab it from the [NIH ftp site](https://goo.gl/TEFNT8)
  * Once you have downloaded the data, concatentate the viral genome sequences:
  ```
  gunzip -c viral.1.1.genomic.fna.gz viral.2.1.genomic.fna.gz > viral.genomic.fna
  ```
  * You then need to format that database using makeblastdb with these parameters:
  ```
  makeblastdb -in viral.genomic.fna -dbtype nucl -title "Viral RefSeq 20180110" -parse_seqids -hash_index
  ```


## Cloning from Git.

To install virus friends you need to clone it from the Git repository;

```
git clone https://github.com/NCBI-Hackathons/VirusFriends.git
```




# EndoVir
Run setup.sh in EndoVir to download all of the databases you will need. You will have to run EndoVir from the work directory.
