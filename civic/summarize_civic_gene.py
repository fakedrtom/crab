from __future__ import print_function
import sys
from collections import defaultdict
from scipy import stats

gene_file = open("tmp.civic_genes.bed", "r")
gene_out = open("civic_genes_summaries.bed", "w")
print("#chromosome\tstart\tstop\tgene\tn_variant\tvariant_IDs\tn_evidence\tevidence_IDs\tmax_evidence\tmax_rating\tevidence_type\tevidence_direction\tclinical_significance\tvariant_origin\tdisease\tmax_score\tcivic_per", file=gene_out)

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
    var_id = line[9] if line[9] != "" else 'none'
    variants[gene].append(var_id)
    var_score = line[11] if line[11] != "" else 'none'
    if var_score != 'none':
        id_score[var_id] = var_score
    evi_type = line[12] if line[12] != "" else 'none'
    types[gene].append(evi_type.rstrip())
    evi_level = line[13] if line[13] != "" else 'none' 
    if evi_level == 'A':
        evi_level = 5
    elif evi_level == 'B':
        evi_level = 4
    elif evi_level == 'C':
        evi_level = 3
    elif evi_level == 'D':
        evi_level = 2
    elif evi_level == 'E':
        evi_level = 1
    elif evi_level == 'none':
        evi_level = 0
    levels[gene].append(evi_level)
    evi_dir = line[14] if line[14] != "" else 'none'
    directions[gene].append(evi_dir.rstrip())
    clin_sig = line[15] if line[15] != "" else 'none'
    clins[gene].append(clin_sig.rstrip())
    rating = line[16] if line[16] != "" else 0
    if rating == 'none':
        rating = 0
    ratings[gene].append(rating)
    evi_id = line[17] if line[17] != "" else 'none'
    evidences[gene].append(evi_id.rstrip())
    origin = line[18] if line[18] != "" else 'none'
    origins[gene].append(origin.rstrip())
    disease = line[19] if line[19] != "" else 'none'
    diseases[gene].append(disease.rstrip())

score_list = []
for id in id_score:
    score_list.append(float(id_score[id]))

for gene in coords:
    max_level = max(levels[gene])
    if max_level == 5:
        max_level = 'A'
    if max_level == 4:
        max_level = 'B'
    if max_level == 3:
        max_level = 'C'
    if max_level == 2:
        max_level = 'D'
    if max_level == 1:
        max_level = 'E'
    if max_level == 0:
        max_level = 'none'
    max_rating = max(ratings[gene])
    num_var = len(set(variants[gene]))
    var_ids = set(variants[gene])
    scores = []
    for id in var_ids:
        if id in id_score:
            scores.append(id_score[id])
    max_score = max(scores) if len(scores) > 0 else 0
    evi_ids = set(evidences[gene])
    if len(evi_ids) > 1 and 'none' in evi_ids:
        evi_ids.remove('none')
    num_evi = len(evi_ids)
    evi_types = set(types[gene])
    if len(evi_types) > 1 and 'none' in evi_types:
        evi_types.remove('none')
    evi_dirs = set(directions[gene])
    if len(evi_dirs) > 1 and 'none' in evi_dirs:
        evi_dirs.remove('none')
    clin_sigs = set(clins[gene])
    if len(clin_sigs) > 1 and 'none' in clin_sigs:
        clin_sigs.remove('none')
    origs = set(origins[gene])
    if len(origs) > 1 and 'none' in origs:
        origs.remove('none')
    subtypes = set(diseases[gene])
    if len(subtypes) > 1 and 'none' in subtypes:
        subtypes.remove('none')
    if max_level == 'none':
        num_evi = 0
    score_per = round(stats.percentileofscore(score_list, float(max_score)),3)
    print("\t".join(coords[gene]) + "\t" + gene + "\t" + str(num_var) + "\t" + ",".join(var_ids) + "\t" + str(num_evi) + "\t" + ",".join(evi_ids) + "\t" + max_level + "\t" + str(max_rating) + "\t" + ",".join(evi_types) + "\t" + ",".join(evi_dirs) + "\t" + ",".join(clin_sigs) + "\t" + ",".join(origs) + "\t" + ",".join(subtypes) + "\t" + str(max_score) + "\t" + str(score_per), file=gene_out)    
