from __future__ import print_function
import sys

cancer_names = open("master_cancer_acronyms.txt", "r")
muts = open("cancer_genes_upon_mutations_or_CNAs.tsv", "r")
muttrans = open("cancer_genes_upon_trans.tsv", "r")
moa = open("gene_MoA.tsv", "r")
gene_coords = open("../ensembl/sorted.ensembl.gene.coords", "r")
out_file = open("ccg.bed", "w")
print("#chromosome\tstart\tend\tgene\ttumorigenesis\talterations\ttranslocations\tcancer_types\tsources", file=out_file)

coords = {}
for i in gene_coords:
    line = i.rsplit("\t")
    chrom = line[0]
    start = line[1]
    end = line[2]
    gene = line[3]
    coords[gene.rstrip()]=[chrom, start, end]

cancers = {}
for line in cancer_names:
    fields = line.rstrip("\n").split("\t")
    cancer = fields[1]
    abr = fields[0]
    cancers[abr] = cancer

actions = {}
for line in moa:
    fields = line.rstrip("\n").split("\t")
    gene = fields[0]
    act = fields[1]
    if act == 'Act':
        act = 'oncogene'
    if act == 'LoF':
        act = 'suppressor'
    actions[gene] = act

genes = []
changes = {}
diseases = {}
trans = {}
sources = {}

for line in muts:
    if line.startswith('gene'):
        continue
    fields = line.rstrip("\n").split("\t")
    gene = fields[0]
    genes.append(gene)
    muttype = fields[1]
    if gene not in changes:
        changes[gene] = []
    changes[gene].append(muttype)
    abr = fields[2]
    if gene not in diseases:
        diseases[gene] = []
    if abr in cancers:
        diseases[gene].append(cancers[abr])
    srcs = fields[3].split(',')
    if gene not in sources:
        sources[gene] = []
    for src in srcs:
        sources[gene].append(src)

for line in muttrans:
    if line.startswith('translocation'):
        continue
    fields = line.rstrip("\n").split("\t")
    trs = fields[0].split('__')
    gene = fields[1]
    genes.append(gene)
    if gene in trs:
        trs.remove(gene)
    if gene not in changes:
        changes[gene] = []
    changes[gene].append('translocation')
    for tran in trs:
        if gene not in trans:
            trans[gene] = []
        trans[gene].append(tran)
    abrs = fields[2].split(';')
    if gene not in diseases:
        diseases[gene] = []
    for abr in abrs:
        if abr in cancers:
            diseases[gene].append(cancers[abr])
    srcs = fields[3].split(';')
    if gene not in sources:
        sources[gene] = []
    for src in srcs:
        sources[gene].append(src)

uniq_genes = set(genes)
for gene in uniq_genes:
    if gene not in actions:
        actions[gene] = 'none'
    if gene in changes:
        uniq_c = set(changes[gene])
    else:
        uniq_c = ['none']
    if gene in trans:
        uniq_t = set(trans[gene])
    else:
        uniq_t = ['none']
    if gene in diseases:
        uniq_d = set(diseases[gene])
    else:
        uniq_d = ['none']
    if gene in sources:
        uniq_s = set(sources[gene])
    else:
        uniq_s = ['none']
    if gene in coords:
        print('\t'.join(coords[gene]) + "\t" + gene + "\t" + actions[gene] + "\t" + ','.join(uniq_c) + "\t" + ','.join(uniq_t) + "\t" + ','.join(uniq_d) + "\t" + ','.join(uniq_s), file=out_file)
