from __future__ import print_function
import sys

tsv = open("cancer_acronyms.tsv", "r")
txt = open("cancer_acronyms.txt", "r")
out_file = open("master_cancer_acronyms.txt", "w")

master = {}
cols = {}
for line in tsv:
    fields = line.rstrip("\n").split("\t")
    if fields[0] == 'cancer_acronym':
        cols = dict(zip(fields, range(len(fields))))
        continue
    abr = fields[cols['cancer_acronym']]
    if 'acronym' in abr:
        continue
    cancer = fields[cols['description']]
    new_cancer = []
    for i in cancer:
        if i.isupper():
            i = i.lower()
        new_cancer.append(i)
    master[abr] = ''.join(new_cancer)

cols2 = {}
for line in txt:
    fields = line.rstrip("\n").split("\t")
    if fields[0] == 'acronym':
        cols2 = dict(zip(fields, range(len(fields))))
        continue
    abr = fields[cols2['acronym']]
    if 'acronym' in abr:
        continue
    cancer = fields[cols2['cancer']]
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
