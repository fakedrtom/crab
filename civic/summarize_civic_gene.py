from __future__ import print_function
import sys
from collections import defaultdict

gene_file = open("tmp.civic_genes.bed", "r")
gene_out = open("civic_genes_summaries.bed", "w")
print("#chromosome\tstart\tstop\tgene\tn_variant\tvariant_IDs\tn_evidence\tevidence_IDs\tmax_evidence\tmax_rating\tevidence_type\tevidence_direction\tclinical_significance\tvariant_origin\tdisease\tmax_score", file=gene_out)

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
id_score = {}

for i in gene_file:
    line = i.rsplit("\t")
    chrom = line[0]
    start = line[1]
    end = line[2]
    gene = line[3]
    coords[gene]=[chrom, start, end]
    var_id = line[9] if line[9] != "" else 'None'
    variants[gene].append(var_id)
    var_score = line[11] if line[11] != "" else 'None'
    id_score[var_id] = var_score
    evi_type = line[12] if line[12] != "" else 'None'
    types[gene].append(evi_type.rstrip())
    evi_level = line[13] if line[13] != "" else 'None' 
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
    evi_dir = line[14] if line[14] != "" else 'None'
    directions[gene].append(evi_dir.rstrip())
    clin_sig = line[15] if line[15] != "" else 'None'
    clins[gene].append(clin_sig.rstrip())
    rating = line[16] if line[16] != "" else 0
    ratings[gene].append(rating)
    evi_id = line[17] if line[17] != "" else 'None'
    evidences[gene].append(evi_id.rstrip())
    origin = line[18] if line[18] != "" else 'None'
    origins[gene].append(origin.rstrip())
    disease = line[19] if line[19] != "" else 'None'
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
    scores = []
    for id in var_ids:
        scores.append(id_score[id])
    max_score = max(scores)
    evi_ids = set(evidences[gene])
    if len(evi_ids) > 1 and 'None' in evi_ids:
        evi_ids.remove('None')
    num_evi = len(evi_ids)
    evi_types = set(types[gene])
    if len(evi_types) > 1 and 'None' in evi_types:
        evi_types.remove('None')
    evi_dirs = set(directions[gene])
    if len(evi_dirs) > 1 and 'None' in evi_dirs:
        evi_dirs.remove('None')
    clin_sigs = set(clins[gene])
    if len(clin_sigs) > 1 and 'None' in clin_sigs:
        clin_sigs.remove('None')
    origs = set(origins[gene])
    if len(origs) > 1 and 'None' in origs:
        origs.remove('None')
    subtypes = set(diseases[gene])
    if len(subtypes) > 1 and 'None' in subtypes:
        subtypes.remove('None')
    if max_level is 'None':
        num_evi = 0
    print("\t".join(coords[gene]) + "\t" + gene + "\t" + str(num_var) + "\t" + ",".join(var_ids) + "\t" + str(num_evi) + "\t" + ",".join(evi_ids) + "\t" + max_level + "\t" + str(max_rating) + "\t" + ",".join(evi_types) + "\t" + ",".join(evi_dirs) + "\t" + ",".join(clin_sigs) + "\t" + ",".join(origs) + "\t" + ",".join(subtypes) + "\t" + str(max_score), file=gene_out)    
