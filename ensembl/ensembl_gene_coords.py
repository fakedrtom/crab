import sys
from collections import defaultdict

#Create a list of Ensembl gene coords with gene names
#Genes with alternate names have coord created for each
#alternate name

#Latest ensGene Primary Table from UCSC
ensembl = open("ensGene.txt", "r")

#Latest ensemblToGeneName Primary Table from UCSC
gene_names = open("ensemblToGeneName.txt", "r")

#EntrezGene alternate names
syn_names = open("entrez_gene_synonyms.txt", "r")

#Create dictionary of Ensembl gene IDs and the gene names
names = {}
for line in gene_names:
    if not line.startswith("#"):
        entry = line.rsplit("\t")
        enst_id = entry[0]
        gene = entry[1].rstrip()
        names[enst_id] = gene

#Create dictionary of Gene names and alternate gene names
alts = {}
for line in syn_names:
    if not line.startswith("#"):
        entry = line.rsplit("\t")
        gene = entry[0]
        syns = entry[1].rstrip().split("|")
        alts[gene] = syns

chroms = {}
coords = defaultdict(list)

#Create dictionary of gene names and all txStart and txEnd 
for line in ensembl:
    if not line.startswith("#"):
        entry = line.rsplit("\t")
        enst_id = entry[1]
        gene = names[enst_id]
        chrom = entry[2]
        start = int(entry[4])
        end = int(entry[5])
        if "_" not in chrom:
            chroms[gene] = chrom
            coords[gene].append(start)
            coords[gene].append(end)

#For each gene print out chrom, min txStart, max txEnd
#If gene has alternate names, do the same for each alternate name
#Also check if gene is an alternate name itself
#If so, print the main gene that the alternate belongs to
#Only print chrom, min txStart, max txEnd, gene name if it hasn't
#all ready been printed 
done = {}
for key in coords:
    chrom = chroms[key].replace("chr", "", 1)
    start = min(coords[key])
    end = max(coords[key])
    print "{a}\t{b}\t{c}\t{d}".format(a=chrom, b=start, c=end, d=key)
    if key not in done:
        done[key] = []
    if key in alts:
        for syn in alts[key]:
            if syn not in alts and syn not in coords:
                if syn not in done:
                    print "{a}\t{b}\t{c}\t{d}".format(a=chrom, b=start, c=end, d=syn)
                    done[syn] = []
    elif key not in alts:
        for gene in alts:
            if key in alts[gene] and gene not in done and gene not in coords:
                print "{a}\t{b}\t{c}\t{d}".format(a=chrom, b=start, c=end, d=gene)
                done[gene] = []
