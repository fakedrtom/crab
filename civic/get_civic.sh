#!/bin/bash

set -euo pipefail

#Get the latest CIViC files
echo "Retrieving the latest data downloads from CIViC"
curl -o nightly-VariantSummaries.tsv -L https://civicdb.org/downloads/nightly/nightly-VariantSummaries.tsv
curl -o nightly-GeneSummaries.tsv -L https://civicdb.org/downloads/nightly/nightly-GeneSummaries.tsv
curl -o nightly-ClinicalEvidenceSummaries.tsv -L https://civicdb.org/downloads/nightly/nightly-ClinicalEvidenceSummaries.tsv

#Merge CIViC files into civic_variants, civic_genes, and civic_genes_summaries bed files
echo "Creating civic_genes, civic_gene_summaries, and civic_variants BED files"
python merge_civic_files.py nightly-ClinicalEvidenceSummaries.tsv nightly-VariantSummaries.tsv nightly-GeneSummaries.tsv ../sorted.ensembl.gene.coords
python summarize_civic_gene.py tmp.civic_genes.bed ../cancer_names_abbreviations.txt
python summarize_civic_variant.py tmp.civic_variants.bed ../cancer_names_abbreviations.txt

#Using gsort, sort and bgzip the bed files, remove the extra, non-gzipped copy of the file
echo "Sorted and gzipping the BED files"
gsort civic_variants_summaries.bed /Users/tom/work/genome_ref/genome.nochr.file | bgzip -c > civic_variants_summaries.bed.gz
rm -r -f civic_variants_summaries.bed
#gsort civic_genes.bed /Users/tom/work/genome_ref/genome.nochr.file | bgzip -c > civic_genes.bed.gz
#rm -r -f civic_genes.bed
gsort civic_genes_summaries.bed /Users/tom/work/genome_ref/genome.nochr.file | bgzip -c > civic_genes_summaries.bed.gz
rm -r -f civic_genes_summaries.bed

#Create an index, using tabix, of the zipped bed files
echo "Creating tabix indices of the BED files"
tabix -p bed civic_variants_summaries.bed.gz
tabix -p bed civic_genes_summaries.bed.gz
