# VirusML
A machine learning approach to identify and validate viruses from metagenomes

Filtering pipeline:
Magic Blast against RefSeqVir (start with a low threshold)
              |
              | Filter on %ID
              |----------------> 97%+, known virus 
              |                 | 
              |           Test for coverage -------> good coverage -> analysis TBD
              |                 | bad coverage is lumped with partials
              v                 v 
            80-96%, partial virus
                      |
                      |
                      v
                Do awesome stuff

Purpose:
Surveying SRA for viral topography 
Expand known viral database to include closely related sequences

Pipeline:
4000 reference viruses as our test dataset
Run through our filtering step above
Assemble contigs from the reads that survive filter
Run flanker to help scaffold these viral seqs

Future directions:
* Instead of RefSeqVir, the reference could be any 

Notes:
Endovir.py is a good reference to base our pipeline
