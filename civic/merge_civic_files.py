from __future__ import print_function
import sys
from collections import defaultdict

evi_file = open("nightly-ClinicalEvidenceSummaries.tsv", "r")
var_file = open("nightly-VariantSummaries.tsv", "r")
sum_file = open("nightly-GeneSummaries.tsv", "r")
gene_coords = open("../ensembl/sorted.ensembl.gene.coords", "r")

variant_out = open("civic_variants.bed", "w")
print("#chromosome\tstart\tstop\tref\talt\tvariant_id\tvariant_types\tcivic_score\tevidence_type\tevidence_level\tevidence_direction\tclinical_significance\trating\tevidence_id\tvariant_origin\tdisease", file=variant_out)
gene_out = open("tmp.civic_genes.bed", "w")

evidence = {}
for i in evi_file:
    line = i.rsplit("\t")
    evi_id = line[17]
    var_id = line[18]
    evidence_type = line[7]
    evidence_level = line[9]
    rating = line[15]
    disease = line[3]
    clinical_significance = line[10]
    evidence_direction = line[8]
    evidence_civic_url = line[35]
    origin = line[33]
    if var_id not in evidence:
        evidence[var_id] = []
    evidence[var_id].append([evidence_type, evidence_level, evidence_direction, clinical_significance, rating, evi_id, origin, disease])

genes_ids = defaultdict(list)
variant = {}
for i in var_file:
    line = i.rsplit("\t")
    if line[0] == 'variant_id':
        continue
    var_id = line[0]
    variant_civic_url = line[1]
    gene = line[2]
    genes_ids[gene].append(var_id)
    chrom = line[7]
    start = int(line[8])-1 if line[8] != ""  else ""
    end = line[9]
    ref = line[10]
    alt = line[11]
    var_type = line[19]
    var_score = line[22].rstrip()
    if var_id not in variant:
        variant[var_id] = []
    variant[var_id].append([chrom, str(start), end, ref, alt, var_id, var_type, var_score])
    if alt is not "":
        if var_id not in evidence:
            print("\t".join(map(str, (chrom, start, end, ref, alt, var_id, var_type, var_score))) + "\t" + "None\tNone\tNone\tNone\tNone\tNone\tNone\tNone", file=variant_out)
        if var_id in evidence:    
            for j in evidence[var_id]:
                print("\t".join(map(str, (chrom, start, end, ref, alt, var_id, var_type, var_score))) + "\t" + "\t".join(j), file=variant_out)

coords = {}
for i in gene_coords:
    line = i.rsplit("\t")
    chrom = line[0]
    start = line[1]
    end = line[2]
    gene = line[3]
    coords[gene.rstrip()]=[chrom, start, end]

for i in sum_file:
    line = i.rsplit("\t")
    gene_civic_url = line[1]
    gene = line[2]
    if gene in coords:
        if gene not in genes_ids:
            print("\t".join(coords[gene]) + "\t" + gene + "\t" + "None\tNone\tNone\tNone\tNone\tNone\tNone\tNone\tNone\tNone\tNone\tNone\tNone\tNone\tNone\tNone", file=gene_out)
        if gene in genes_ids:
            for j in genes_ids[gene]:
                var = variant[j][0]
                if j not in evidence:
                    print("\t".join(coords[gene]) + "\t" + gene + "\t" + "\t".join(var) + "\t" + "None\tNone\tNone\tNone\tNone\tNone\tNone\tNone", file=gene_out)
                if j in evidence:
                    for k in evidence[j]:
                        print("\t".join(coords[gene]) + "\t" + gene + "\t" + "\t".join(var) + "\t" + "\t".join(k), file=gene_out)
