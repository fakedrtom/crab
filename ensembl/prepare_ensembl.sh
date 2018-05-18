#!/bin/bash

#To be used in connection with get_ensembl.sh

set -euo pipefail

#Get the human alternate names from gene_info.gz
#Skip genes without alternate names (column 2 is '-')
echo "Extracting human only gene names with alternates"
gzcat gene_info.gz | awk '$1==9606{print $3"\t"$5}' | awk '$2!="-"' | sort > entrez_gene_synonyms.txt

#Create the Ensembl gene coords list with all alternate names included
echo "Creating sorted.ensembl.gene.coords file"
python ensembl_gene_coords.py | gsort /dev/stdin ~/work/genome_ref/genome.nochr.file > sorted.ensembl.gene.coords

