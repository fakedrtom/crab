Cancer Relevant Annotations Bin (CRAB)
============================================================

Overview
===========================
CRAB is a collection of data from a variety of cancer databases that
has been parsed and summarized into BED or VCF file formats to be used easily
with vcfanno for the annotation of VCF files. CRAB was designed to be 
used alongside [OncoGEMINI](https://github.com/fakedrtom/oncogemini), but
provides a useful resource that can be useful in other applications.

Usage
==========================
Available files through the CRAB are designed to be easily used
alongside [vcfanno](https://github.com/brentp/vcfanno) to add annotations
to VCF files. To quickly get started with vcfanno, the following
is required:

+ Download and install vcfanno (for directions refer to the
[repo](https://github.com/brentp/vcfanno))
+ The source file(s) containing the annotation information that is desired to
be added to a VCF.
+ A vcfanno configuration file that directs vcfanno to the source file(s) and
the desired information within the source file(s) for annotation.

We have provided an example vcfanno configuration file that will
annotate a VCF with information that has been parsed from
[CIViC](https://civicdb.org/home) and the
[CGI](https://www.cancergenomeinterpreter.org/home). To use this
configuration file, download it as well as the source files it uses from
CIViC and CGI:

+ [vcfanno.conf](https://github.com/fakedrtom/crab/blob/master/vcfanno.conf)
+ [civic_genes_summaries.bed.gz](https://github.com/fakedrtom/crab/blob/master/civic/civic_genes_summaries.bed.gz)
+ [civic_variants_summaries.bed.gz](https://github.com/fakedrtom/crab/blob/master/civic/civic_variants_summaries.bed.gz)
+ [ccg.bed.gz](https://github.com/fakedrtom/crab/blob/master/cgi/ccg.bed.gz)
+ [onco_muts.bed.gz](https://github.com/fakedrtom/crab/blob/master/cgi/onco_muts.bed.gz)

Once the files are downloaded be sure to specify the paths to the CIViC and CGI
files in the vcfanno.conf file. With vcfanno installed and all the files in place,
annotate a VCF with vcfanno using a single command:
```
vcfanno vcfanno.config your.vcf.gz > your_annotated.vcf.gz
```
Any number of files can be added to the vcfanno configuration file enabling
great customization to the specific types and quantity of annotations that
can be added to a VCF file.
