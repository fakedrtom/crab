from __future__ import print_function
import sys
from collections import defaultdict

#evi_file = open("nightly-ClinicalEvidenceSummaries.tsv", "r")
evi_file = open(sys.argv[1], "r")
#var_file = open("nightly-VariantSummaries.tsv", "r")
var_file = open(sys.argv[2], "r")
#sum_file = open("nightly-GeneSummaries.tsv", "r")
sum_file = open(sys.argv[3], "r")
#gene_coords = open("../ensembl/sorted.ensembl.gene.coords", "r")
gene_coords = open(sys.argv[4], "r")

variant_out = open("tmp.civic_variants.bed", "w")
#print("#chromosome\tstart\tstop\tref\talt\tvariant_id\tvariant_types\tcivic_score\tevidence_type\tevidence_level\tevidence_direction\tclinical_significance\trating\tevidence_id\tvariant_origin\tdisease", file=variant_out)
gene_out = open("tmp.civic_genes.bed", "w")

evidence = {}
evi_cols = {}
for i in evi_file:
    line = i.rstrip("\n").split("\t")
    if line[0] == 'gene':
        evi_cols = dict(zip(line, range(len(line))))
        continue
    evi_id = line[evi_cols['evidence_id']]
    var_id = line[evi_cols['variant_id']]
    evidence_type = line[evi_cols['evidence_type']]
    evidence_level = line[evi_cols['evidence_level']]
    rating = line[evi_cols['rating']]
    disease = line[evi_cols['disease']]
    clinical_significance = line[evi_cols['clinical_significance']]
    evidence_direction = line[evi_cols['evidence_direction']]
    evidence_civic_url = line[evi_cols['evidence_civic_url']]
    origin = line[evi_cols['variant_origin']]
    if var_id not in evidence:
        evidence[var_id] = []
    evidence[var_id].append([evidence_type, evidence_level, evidence_direction, clinical_significance, rating, evi_id, origin, disease])

genes_ids = defaultdict(list)
variant = {}
var_cols = {}
for i in var_file:
    line = i.rstrip("\n").split("\t")
    if line[0] == 'variant_id':
        var_cols = dict(zip(line, range(len(line))))
        continue
    var_id = line[var_cols['variant_id']]
    variant_civic_url = line[var_cols['variant_civic_url']]
    gene = line[var_cols['gene']]
    genes_ids[gene].append(var_id)
    chrom = line[var_cols['chromosome']]
    start = int(line[var_cols['start']])-1 if line[var_cols['start']] != ""  else ""
    end = line[var_cols['stop']]
    ref = line[var_cols['reference_bases']]
    alt = line[var_cols['variant_bases']]
    var_type = line[var_cols['variant_types']]
    var_score = line[var_cols['civic_variant_evidence_score']]
    if len(var_score.split(' ')) > 1:
        var_score = 'none'
    if var_id not in variant:
        variant[var_id] = []
    variant[var_id].append([chrom, str(start), end, ref, alt, var_id, var_type, var_score])
    if alt is not "":
        if var_id not in evidence:
            print("\t".join(map(str, (chrom, start, end, ref, alt, var_id, var_type, var_score))) + "\t" + "none\tnone\tnone\tnone\tnone\tnone\tnone\tnone", file=variant_out)
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

sum_cols = {}
for i in sum_file:
    line = i.rstrip("\n").split("\t")
    if line[0] == 'gene_id':
        sum_cols = dict(zip(line, range(len(line))))
        continue
    gene_civic_url = line[sum_cols['gene_civic_url']]
    gene = line[sum_cols['name']]
    if gene in coords:
        if gene not in genes_ids:
            print("\t".join(coords[gene]) + "\t" + gene + "\t" + "none\tnone\tnone\tnone\tnone\tnone\tnone\tnone\tnone\tnone\tnone\tnone\tnone\tnone\tnone\tnone", file=gene_out)
        if gene in genes_ids:
            for j in genes_ids[gene]:
                var = variant[j][0]
                if j not in evidence:
                    print("\t".join(coords[gene]) + "\t" + gene + "\t" + "\t".join(var) + "\t" + "none\tnone\tnone\tnone\tnone\tnone\tnone\tnone", file=gene_out)
                if j in evidence:
                    for k in evidence[j]:
                        print("\t".join(coords[gene]) + "\t" + gene + "\t" + "\t".join(var) + "\t" + "\t".join(k), file=gene_out)
