#!/bin/bash

set -euo pipefail

#Get the latest CGI files
echo "Retrieving the latest data downloads from CGI"
curl -o catalog_of_validated_oncogenic_mutations_latest.zip -L https://www.cancergenomeinterpreter.org/data/catalog_of_validated_oncogenic_mutations_latest.zip?ts=20180216
unzip -o catalog_of_validated_oncogenic_mutations_latest.zip
curl -o catalog_of_cancer_genes_latest.zip -L https://www.cancergenomeinterpreter.org/data/catalog_of_cancer_genes_latest.zip
unzip -o catalog_of_cancer_genes_latest.zip

#Create a master cancer acronyms file and merge/parse files into BEDs
echo "Creating master_cancer_acronyms.txt, and ccg, onco_muts BED files"
python make_master_acronyms.py
python make_gene_beds.py
python make_onco_mutations_bed.py

#Using gsort, sort and bgzip the bed files, remove the extra, non-gzipped copy of the file
echo "Sorted and gzipping the BED files"
gsort ccg.bed /Users/tom/work/genome_ref/genome.nochr.file | bgzip -c > ccg.bed.gz
rm -r -f ccg.bed
gsort onco_muts.bed /Users/tom/work/genome_ref/genome.nochr.file | bgzip -c > onco_muts.bed.gz
rm -r -f onco_muts.bed

#Create an index, using tabix, of the zipped bed files
echo "Creating tabix indices of the BED files"
tabix -p bed ccg.bed.gz
tabix -p bed onco_muts.gz
