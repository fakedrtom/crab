from __future__ import print_function
import sys
from collections import defaultdict

cats_file = open("dgidb.categories.tsv", "r")
ints_file = open("dgidb.interactions.tsv", "r")
gene_coords = open("../ensembl/sorted.ensembl.gene.coords", "r")

file_out = open("dgidb.summaries.bed", "w")
print("#chromosome\tstart\tstop\tgene\tdrug\tinteraction\tcategories", file=file_out)

category = {}
cat_cols = {}
for i in cats_file:
    line = i.rstrip("\n").split("\t")
    if line[0] == 'entrez_gene_symbol':
        cat_cols = dict(zip(line, range(len(line))))
    gene = line[cat_cols['entrez_gene_symbol']]
    cat = line[cat_cols['category']]
    if gene not in category:
        category[gene] = []
    category[gene].append(cat)

genes_ids = defaultdict(list)
interaction = {}
drugs = {}
int_cols = {}
for i in ints_file:
    line = i.rstrip("\n").split("\t")
    if line[0] == 'gene_name':
        int_cols = dict(zip(line, range(len(line))))
    gene = line[int_cols['gene_name']] if line[int_cols['gene_name']] != ""  else "none"
    inter = line[int_cols['interaction_types']] if line[int_cols['interaction_types']] != ""  else "none"
    drug = line[int_cols['drug_name']] if line[int_cols['drug_name']] != ""  else "none"
    if gene not in interaction:
        interaction[gene] = []
    interaction[gene].append(inter)
    if gene not in drugs:
        drugs[gene] = []
    drugs[gene].append(drug)

coords = {}
for i in gene_coords:
    line = i.rsplit("\t")
    chrom = line[0]
    start = line[1]
    end = line[2]
    gene = line[3]
    coords[gene.rstrip()]=[chrom, start, end]

for key in coords:
    cats = ['none']
    if key in category:
        cats = set(category[key])
    ints = ['none']
    if key in interaction:
        ints = set(interaction[key])
    drgs = ['none']
    if key in drugs:
        drgs = set(drugs[key])
    if key in category or key in interaction or key in drugs:
        print("\t".join(coords[key]) + "\t" + key + "\t" + ",".join(sorted(drgs)) + "\t" + ",".join(sorted(ints)) + "\t" + ",".join(sorted(cats)), file=file_out)
