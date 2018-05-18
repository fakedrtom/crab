#!/bin/bash

set -euo pipefail

#Get the latest Ensembl gene files
echo "Retrieving Ensembl gene files and Entrez Gene Info"
curl -o ensGene.txt.gz -L http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/ensGene.txt.gz
curl -o ensemblToGeneName.txt.gz -L http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/ensemblToGeneName.txt.gz
curl -o gene_info.gz -L ftp://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz

#Unzip Ensembl files
echo "Unzipping Ensembl gene files"
gunzip -f ensGene.txt.gz
gunzip -f ensemblToGeneName.txt.gz
