from __future__ import print_function
import sys
from collections import defaultdict
from scipy import stats

var_file = open("tmp.civic_variants.bed", "r")
var_out = open("civic_variants_summaries.bed", "w")
abbrs = open("/Users/tom/src/cancer_annotations/cancer_names_abbreviations.txt", "r")
print("#chromosome\tstart\tstop\tref\talt\tvariant_ID\tvariant_type\tcivic_score\tcivic_per\tn_evidence\tevi_IDs\tevi_types\tmax_level\tevi_directions\tclin_sigs\tmax_rating\torigins\tdiseases\tabbreviations", file=var_out)

coords = {}
evidences = defaultdict(list)
levels = defaultdict(list)
ratings = defaultdict(list)
types = defaultdict(list)
directions = defaultdict(list)
clins = defaultdict(list)
origins = defaultdict(list)
diseases = defaultdict(list)
id_score = {}

for i in var_file:
    line = i.rstrip("\n").rsplit("\t")
    chrom = line[0]
    start = line[1]
    end = line[2]
    ref = line[3]
    alt = line[4]
    varid = line[5]
    vartype = line[6] if line[6] != "" else 'none'
    score = line[7]
    if score != 'none':
        id_score[varid] = score
    coords[varid]=[chrom, start, end, ref, alt, varid, vartype, score]
    evi_type = line[8] if line[8] != "" else 'none'
    types[varid].append(evi_type.rstrip())
    evi_level = line[9] if line[9] != "" else 'none' 
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
    elif evi_level is 'none':
        evi_level = 0
    levels[varid].append(evi_level)
    evi_dir = line[10] if line[10] != "" else 'none'
    directions[varid].append(evi_dir.rstrip())
    clin_sig = line[11] if line[11] != "" else 'none'
    clins[varid].append(clin_sig.rstrip())
    rating = line[12] if line[12] != "" else 0
    ratings[varid].append(rating)
    evi_id = line[13] if line[13] != "" else 'none'
    evidences[varid].append(evi_id.rstrip())
    origin = line[14] if line[14] != "" else 'none'
    origins[varid].append(origin.rstrip())
    disease = line[15] if line[15] != "" else 'none'
    diseases[varid].append(disease.rstrip())

scores = []
for id in id_score:
    scores.append(float(id_score[id]))

cancers = {}
for line in abbrs:
    names = line.rstrip("\n").split("\t")
    cancers[names[0]] = names[1]
    
for id in coords:
    max_level = max(levels[id])
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
        max_level = 'none'
    max_rating = max(ratings[id])
    evi_ids = set(evidences[id])
    if len(evi_ids) > 1 and 'none' in evi_ids:
        evi_ids.remove('none')
    num_evi = len(evi_ids)
    evi_types = set(types[id])
    if len(evi_types) > 1 and 'none' in evi_types:
        evi_types.remove('none')
    evi_dirs = set(directions[id])
    if len(evi_dirs) > 1 and 'none' in evi_dirs:
        evi_dirs.remove('none')
    clin_sigs = set(clins[id])
    if len(clin_sigs) > 1 and 'none' in clin_sigs:
        clin_sigs.remove('none')
    origs = set(origins[id])
    if len(origs) > 1 and 'none' in origs:
        origs.remove('none')
    subtypes = set(diseases[id])
    if len(subtypes) > 1 and 'none' in subtypes:
        subtypes.remove('none')
    abbr = []
    for s in subtypes:
        if s == 'none':
            abbr.append(s)
        else:
            if s.lower() in cancers:
                abbr.append(cancers[s.lower()])
            if s.lower() not in cancers:
                print(s.lower()+' not recognized')
    if max_level == 'none':
        num_evi = 0
    score_per = round(stats.percentileofscore(scores, float(coords[id][7])),3)
    print("\t".join(coords[id]) + "\t" + str(score_per) + "\t" + str(num_evi) + "\t" + ",".join(sorted(evi_ids)) + "\t" + ",".join(sorted(evi_types)) + "\t" + max_level + "\t" + ",".join(sorted(evi_dirs)) + "\t" + ','.join(sorted(clin_sigs)) + "\t" + str(max_rating) + "\t" + ",".join(sorted(origs)) + "\t" + ",".join(sorted(subtypes)) + "\t" + ",".join(sorted(set(abbr))), file=var_out)
