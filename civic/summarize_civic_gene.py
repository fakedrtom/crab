from __future__ import print_function
import sys
from collections import defaultdict

gene_file = open("tmp.civic_genes.bed", "r")
gene_out = open("civic_genes_summaries.bed", "w")
print("#chromosome\tstart\tstop\tgene\tn_variant\tvariant_IDs\tn_evidence\tevidence_IDs\tmax_evidence\tmax_rating\tevidence_type\tevidence_direction\tclinical_significance\tvariant_origin\tdisease", file=gene_out)

coords = {}
variants = defaultdict(list)
evidences = defaultdict(list)
levels = defaultdict(list)
ratings = defaultdict(list)
types = defaultdict(list)
directions = defaultdict(list)
clins = defaultdict(list)
origins = defaultdict(list)
diseases = defaultdict(list)

for i in gene_file:
    line = i.rsplit("\t")
    chrom = line[0]
    start = line[1]
    end = line[2]
    gene = line[3]
    coords[gene]=[chrom, start, end]
    var_id = line[9] if line[9] != "" else 'None'
    variants[gene].append(var_id)
    evi_level = line[12] if len(line) > 12 else 'None' 
    if evi_level is 'A':
        evi_level = 5
    elif evi_level is 'B':
        evi_level = 4
    elif evi_level is 'C':
        evi_level = 3
    elif evi_level is 'D':
        evi_level = 2
    elif evi_level is 'E':
        evi_level = 1
    elif evi_level is 'None':
        evi_level = 0
    levels[gene].append(evi_level)
    rating = line[15] if len(line) > 15 else 0
    ratings[gene].append(rating)
    evi_id = line[16] if len(line) > 16 else 'None'
    evidences[gene].append(evi_id.rstrip())
    evi_type = line[11] if len(line) > 11 else 'None'
    types[gene].append(evi_type.rstrip())
    evi_dir = line[13] if len(line) > 13 else 'None'
    directions[gene].append(evi_dir.rstrip())
    clin_sig = line[14] if len(line) > 14 else 'None'
    clins[gene].append(clin_sig.rstrip())
    origin = line[17] if len(line) > 17 else 'None'
    origins[gene].append(origin.rstrip())
    disease = line[18] if len(line) > 18 else 'None'
    diseases[gene].append(disease.rstrip())

for gene in coords:
    max_level = max(levels[gene])
    if max_level is 5:
        max_level = 'A'
    if max_level is 4:
        max_level = 'B'
    if max_level is 3:
        max_level = 'C'
    if max_level is 2:
        max_level = 'D'
    if max_level is 1:
        max_level = 'E'
    if max_level is 0:
        max_level = 'None'
    max_rating = max(ratings[gene])
    num_var = len(set(variants[gene]))
    var_ids = set(variants[gene])
    num_evi = len(set(evidences[gene]))
    evi_ids = set(evidences[gene])
    evi_types = set(types[gene])
    evi_dirs = set(directions[gene])
    clin_sigs = set(clins[gene])
    origs = set(origins[gene])
    subtypes = set(diseases[gene])
    if max_level is 'None':
        num_evi = 0
    print("\t".join(coords[gene]) + "\t" + gene + "\t" + str(num_var) + "\t" + ",".join(var_ids) + "\t" + str(num_evi) + "\t" + ",".join(evi_ids) + "\t" + max_level + "\t" + str(max_rating) + "\t" + ",".join(evi_types) + "\t" + ",".join(evi_dirs) + "\t" + ",".join(clin_sigs) + "\t" + ",".join(origs) + "\t" + ",".join(subtypes), file=gene_out)    
