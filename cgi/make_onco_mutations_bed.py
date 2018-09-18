from __future__ import print_function
import sys

file = open("catalog_of_validated_oncogenic_mutations.tsv", "r")
gene_coords = open("../ensembl/sorted.ensembl.gene.coords", "r")
cancer_names = open("master_cancer_acronyms.txt", "r")

out_file = open("onco_muts.bed", "w")
print("#chromosome\tstart\tend\tref\talt\tgene\tmutation_type\tcancer_types\tsources", file=out_file)

cancers = {}
for line in cancer_names:
    fields = line.rstrip("\n").split("\t")
    cancer = fields[1]
    abr = fields[0]
    cancers[abr] = cancer

for line in file:
    if line.startswith("gene"):
        continue
    fields = line.rstrip("\n").split("\t")
    gene = fields[0]
    ghgvs = fields[1].split('__')
    ppos = fields[2]
    trans = fields[3]
    info = fields[4]
    muttype = fields[5]
    abrs = fields[6].split('__')
    sources = fields[7].split('__')
    reference = fields[8]
    for var in ghgvs:
        if 'del' not in var and 'dup' not in var and 'ins' not in var and '>' in var:
            fix = var.split(':g.')
            chrom = fix[0][3:]
            alleles = fix[1][-3:].split('>')
            ref = alleles[0]
            alt = alleles[1]
            pos = fix[1][:-3]
            start = int(pos)-1
            end = pos
            coord = [chrom, str(start), str(end), ref, alt]
            cancer_types = []
            for abr in abrs:
                if abr not in cancers:
                    continue
                cancer_types.append(cancers[abr])
            print("\t".join(coord) + "\t" + gene + "\t" + muttype + "\t" + ",".join(cancer_types) + "\t" + ','.join(sources), file=out_file)
