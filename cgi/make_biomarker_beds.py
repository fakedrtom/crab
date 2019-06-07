from __future__ import print_function
import sys

file = open("cgi_biomarkers_per_variant.tsv", "r")
gene_coords = open("../ensembl/sorted.ensembl.gene.coords", "r")

var_out = open("biomarkers_variant.bed", "w")
print("#chromosome\tstart\tend\tref\talt\tdrug\tdrug_status\tevidence_level\tassociation\tsource\tprimary_tumor\tmetastatic_tumor\ttarget", file=var_out)
gene_out = open("biomarkers_gene.bed", "w")
print("#chromosome\tstart\tend\tgene\tdrugs\tdiseases\tsources", file=gene_out)

drugs = {}
cancers = {}
sources = {}

for line in file:
    if line.startswith("Alteration"):
        continue
    data = line.rstrip("\n").split("\t")
    association = data[3] if data[3] != "" else 'none'
    drug = data[8].replace('[', '').replace(']', '').replace(';', ',') if data[8] != '[]' else 'none'
    status = data[11] if data[11] != "" else 'none'
    evi_level = data[12] if data[12] != "" else 'none'
    gene = data[13]
    meta = data[14] if data[14] != "" else 'none'
    prim = data[27] if data[27] != "" else 'none'
    source = data[17].replace(';', ',') if data[17] != "" else 'none'
    target = data[19] if data[19] != "" else 'none'
    var_info = data[21].split(":g.") if data[21] != "" else 'none'
    if var_info != 'none' and var_info[0] != 'gDNA':
        chrom = var_info[0][3:]
        if '>' in var_info[1]:
            alleles = var_info[1][-3:].split('>')
            ref = alleles[0]
            alt = alleles[1]
            pos = var_info[1][:-3]
            start = int(pos)-1
            end = pos
        elif 'del' in var_info[1]:
            fix = var_info[1].replace('ins', 'del').split('del')
            ref = fix[1]
            alt = fix[2]
            pos = fix[0].split('_')
            start = int(pos[0])-1
            end = pos[1]
        print(chrom + "\t" + str(start) + "\t" + str(end) + "\t" + ref + "\t" + alt + "\t" + drug + "\t" + status + "\t" + evi_level + "\t" + association + "\t" + source + "\t" + prim + "\t" + meta + "\t" + target, file=var_out)
    if gene not in drugs:
        drugs[gene] = []
    drugs[gene].append(drug)
    if gene not in cancers:
        cancers[gene] = []
    cancers[gene].append(meta)
    cancers[gene].append(prim)
    if gene not in sources:
        sources[gene] = []
    sources[gene].append(source)
        
coords = {}
for i in gene_coords:
    line = i.rsplit("\t")
    chrom = line[0]
    start = line[1]
    end = line[2]
    gene = line[3]
    coords[gene.rstrip()]=[chrom, start, end]

for key in coords:
    drgs = ['none']
    if key in drugs:
        drgs = set(drugs[key])
    if len(drgs) > 1 and 'none' in drgs:
        drgs.remove('none')
    cnrs = ['none']
    if key in cancers:
        cnrs = set(cancers[key])
    if len(cnrs) > 1 and 'none' in cnrs:
        cnrs.remove('none')
    srcs = ['none']
    if key in sources:
        srcs = set(sources[key])
    if len(srcs) > 1 and 'none' in srcs:
        srcs.remove('none')
    if key in drugs or key in cancers or key in sources:
        print("\t".join(coords[key]) + "\t" + key + "\t" + ",".join(drgs) + "\t" + ",".join(cnrs) + "\t" + ",".join(srcs), file=gene_out)
