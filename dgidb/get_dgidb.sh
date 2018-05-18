#!/bin/bash

set -euo pipefail

#Get the latest DGIdb files
echo "Retrieving DGIdb files"
curl -o dgidb.interactions.tsv -L http://www.dgidb.org/data/interactions.tsv
curl -o dgidb.categories.tsv -L http://www.dgidb.org/data/categories.tsv

#Merge DGIdb files into dgidb.summaries.bed file
echo "Created BED file for DGIdb files"
python merge_dgidb_files.py

#Using gsort, sort and bgzip the bed file
echo "Sorting and gzipping the BED file"
gsort dgidb.summaries.bed ~/work/genome_ref/genome.nochr.file | bgzip -c > dgidb.summaries.bed.gz
rm -r -f dgidb.summaries.bed

#Create an index, using tabix, of the zipped bed files
echo "Creating tabix index of the BED file"
tabix -p bed dgidb.summaries.bed.gz
