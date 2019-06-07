from __future__ import print_function
import sys

cancer_names = open("master_cancer_acronyms.txt", "r")
muts = open("cancer_genes_upon_mutations_or_CNAs.tsv", "r")
muttrans = open("cancer_genes_upon_trans.tsv", "r")
moa = open("gene_MoA.tsv", "r")
gene_coords = open("../ensembl/sorted.ensembl.gene.coords", "r")
out_file = open("ccg.bed", "w")
print("#chromosome\tstart\tend\tgene\ttumorigenesis\talterations\ttranslocations\tcancer_types\tabbreviations\tsources", file=out_file)

coords = {}
for i in gene_coords:
    line = i.rsplit("\t")
    chrom = line[0]
    start = line[1]
    end = line[2]
    gene = line[3]
    coords[gene.rstrip()]=[chrom, start, end]

cancers = {}
rev_cancers = {}
for line in cancer_names:
    fields = line.rstrip("\n").split("\t")
    cancer = fields[1]
    abr = fields[0]
    cancers[abr] = cancer
    rev_cancers[cancer] = abr

actions = {}
act_cols = {}
for line in moa:
    fields = line.rstrip("\n").split("\t")
    if fields[0] == 'gene':
        act_cols = dict(zip(fields, range(len(fields))))
        continue
    gene = fields[act_cols['gene']]
    act = fields[act_cols['gene_MoA']]
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
mut_cols = {}

for line in muts:
    fields = line.rstrip("\n").split("\t")
    if fields[0] == 'gene':
        mut_cols = dict(zip(fields, range(len(fields))))
        continue
    gene = fields[mut_cols['gene']]
    genes.append(gene)
    muttype = fields[mut_cols['alteration']]
    if gene not in changes:
        changes[gene] = []
    changes[gene].append(muttype)
    abr = fields[mut_cols['cancer_acronym']]
    if gene not in diseases:
        diseases[gene] = []
    if abr in cancers:
        diseases[gene].append(cancers[abr])
    srcs = fields[mut_cols['source']].split(',')
    if gene not in sources:
        sources[gene] = []
    for src in srcs:
        sources[gene].append(src)

trn_cols = {}

for line in muttrans:
    fields = line.rstrip("\n").split("\t")
    if fields[0] == 'translocation':
        trn_cols = dict(zip(fields, range(len(fields))))
        continue
    trs = fields[trn_cols['translocation']].split('__')
    gene = fields[trn_cols['effector_gene']]
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
    abrs = fields[trn_cols['cancer_acronym']].split(';')
    if gene not in diseases:
        diseases[gene] = []
    for abr in abrs:
        if abr in cancers:
            diseases[gene].append(cancers[abr])
    srcs = fields[trn_cols['source']].split(';')
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
    abbr = []
    for s in uniq_d:
        if s == 'none':
            abbr.append(s)
        else:
            if s.lower() in rev_cancers:
                abbr.append(rev_cancers[s.lower()])
            if s.lower() not in rev_cancers:
                print(s.lower()+' not recognized')
    if gene in sources:
        uniq_s = set(sources[gene])
    else:
        uniq_s = ['none']
    if gene in coords:
        print('\t'.join(coords[gene]) + "\t" + gene + "\t" + actions[gene] + "\t" + ','.join(sorted(uniq_c)) + "\t" + ','.join(sorted(uniq_t)) + "\t" + ','.join(sorted(uniq_d)) + "\t" + ",".join(sorted(set(abbr))) + "\t" + ','.join(sorted(uniq_s)), file=out_file)
