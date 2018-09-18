from __future__ import print_function
import sys

tsv = open("cancer_acronyms.tsv", "r")
txt = open("cancer_acronyms.txt", "r")
out_file = open("master_cancer_acronyms.txt", "w")

master = {}

for line in tsv:
    fields = line.rstrip("\n").split("\t")
    abr = fields[0]
    if 'acronym' in abr:
        continue
    cancer = fields[1]
    new_cancer = []
    for i in cancer:
        if i.isupper():
            i = i.lower()
        new_cancer.append(i)
    master[abr] = ''.join(new_cancer)

for line in txt:
    fields = line.rstrip("\n").split("\t")
    abr= fields[0]
    if 'acronym' in abr:
        continue
    cancer = fields[1]
    new_cancer = []
    for i in cancer:
        if i.isupper():
            i =i.lower()
        new_cancer.append(i)
    master[abr] = ''.join(new_cancer)

abrlist = master.keys()
abrlist.sort()
for abr in abrlist:
    print(abr + "\t" + master[abr], file=out_file)
