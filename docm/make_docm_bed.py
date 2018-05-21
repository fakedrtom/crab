import sys

docm = open("docm.tsv", "r")

print("#chromosome\tstart\tstop\tref\talt\tgene\tmutation_type\tdiseases\tpubmed_sources")
for line in docm:
    fields = line.rstrip("\n").split("\t")
    chrom = fields[1]
    if chrom == 'chromosome':
        continue
    start = int(fields[2]) - 1
    end = fields[3]
    ref = fields[4]
    alt = fields[5]
    gene = fields[7]
    mut_type = fields[8]
    diseases = fields[10]
    pubmeds = fields[11]
    data_list = [chrom, str(start), end, ref, alt, gene, mut_type, diseases, pubmeds]
    print "\t".join(data_list)

