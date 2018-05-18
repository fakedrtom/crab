from __future__ import print_function
import sys
from collections import defaultdict

cats_file = open("dgidb.categories.tsv", "r")
ints_file = open("dgidb.interactions.tsv", "r")
gene_coords = open("sorted.ensembl.gene.coords", "r")

file_out = open("dgidb.summaries.bed", "w")
print("#chromosome\tstart\tstop\tgene\tdrug\tinteraction\tcategories", file=file_out)

category = {}
for i in cats_file:
    line = i.rsplit("\t")
    gene = line[0]
    cat = line[3].rstrip()
    if gene not in category:
        category[gene] = []
    category[gene].append(cat)

genes_ids = defaultdict(list)
interaction = {}
drugs = {}
for i in ints_file:
    line = i.rsplit("\t")
    gene = line[0] if line[0] != ""  else "none"
    inter = line[4] if line[4] != ""  else "none"
    drug = line[7] if line[7] != ""  else "none"
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
        print("\t".join(coords[key]) + "\t" + key + "\t" + ",".join(drgs) + "\t" + ",".join(ints) + "\t" + ",".join(cats), file=file_out)
