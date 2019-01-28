#Create a vcfanno.conf file
DIR=`pwd`

#Adding CIViC
echo '[[annotation]]' > vcfanno.conf
echo 'file="'$DIR'/civic/civic_genes_summaries.bed.gz"' >> vcfanno.conf
echo 'columns=[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]' >> vcfanno.conf
echo 'names=["civic_gene","civic_gene_n_vars","civic_gene_var_ids","civic_gene_n_evis","civic_gene_evi_ids","civic_gene_max_level","civic_gene_max_rating","civic_gene_evi_types","civic_gene_evi_directions","civic_gene_clin_sigs","civic_gene_origins","civic_gene_diseases","civic_gene_abbreviations","civic_gene_max_score","civic_gene_percentile"]' >> vcfanno.conf
echo 'ops=["self","max","self","max","self","self","max","self","self","self","self","self","self","max","max"]' >> vcfanno.conf
printf "\n" >> vcfanno.conf
echo '[[annotation]]' >> vcfanno.conf
echo 'file="'$DIR'/civic/civic_variants_summaries.bed.gz"' >> vcfanno.conf
echo 'columns=[6,6,8,9,12,13,14,15,16,11,17,18,19]' >> vcfanno.conf
echo 'names=["in_civic","civic_var_id","civic_score","civic_percentile","civic_evi_type","civic_evi_level","civic_evi_direction","civic_clin_sig","civic_rating","civic_evi_id","civic_var_origin","civic_disease","civic_abbreviations"]' >> vcfanno.conf
echo 'ops=["flag","concat","concat","concat","concat","concat","concat","concat","concat","concat", "concat", "concat","concat"]' >> vcfanno.conf

#Adding DGIdb
printf "\n" >> vcfanno.conf
echo '[[annotation]]' >> vcfanno.conf
echo 'file="'$DIR'/dgidb/dgidb.summaries.bed.gz"' >> vcfanno.conf
echo 'columns=[4,5,6,7]' >> vcfanno.conf
echo 'names=["dgidb_gene","dgidb_drug","dgidb_interaction","dgidb_categories"]' >> vcfanno.conf
echo 'ops=["self","self","self","self"]' >> vcfanno.conf

#Adding DoCM
printf "\n" >> vcfanno.conf
echo '[[annotation]]' >> vcfanno.conf
echo 'file="'$DIR'/docm/docm.bed.gz"' >> vcfanno.conf
echo 'columns=[6,6,7,8,9]' >> vcfanno.conf
echo 'names=["in_docm","docm_gene","docm_mutation_type","docm_disease","docm_pubmed"]' >> vcfanno.conf
echo 'ops=["flag","self","self","self","self"]' >> vcfanno.conf

#Adding CGI
printf "\n" >> vcfanno.conf
echo '[[annotation]]' >> vcfanno.conf
echo 'file="'$DIR'/cgi/onco_muts.bed.gz"' >> vcfanno.conf
echo 'columns=[6,7,8,9,10]' >> vcfanno.conf
echo 'names=["in_cgi", "cgi_mutation_type", "cgi_cancer_types", "cgi_abbreviations", "cgi_reported_by"]' >> vcfanno.conf
echo 'ops=["flag", "self", "self", "self", "self"]' >> vcfanno.conf
printf "\n" >> vcfanno.conf
echo '[[annotation]]' >> vcfanno.conf
echo 'file="'$DIR'/cgi/ccg.bed.gz"' >> vcfanno.conf
echo 'columns=[4,5,6,7,8,9,10]' >> vcfanno.conf
echo 'names=["cgi_gene", "cgi_gene_tumorigenesis", "cgi_gene_alterations", "cgi_gene_translocations", "cgi_gene_cancer_types", "cgi_gene_abbreviations", "cgi_gene_sources"]' >> vcfanno.conf
echo 'ops=["self", "self", "self", "self", "self", "self", "self"]' >> vcfanno.conf

#Adding CHASMPLUS
printf "\n" >> vcfanno.conf
echo '[[annotation]]' >> vcfanno.conf
echo 'file="'$DIR'/chasmplus.vcf.gz"' >> vcfanno.conf
echo 'fields=["CHASM_PVALUE", "CHASM_SCORE"]' >> vcfanno.conf
echo 'names=["chasmplus_pvalue", "chasmplus_score"]' >> vcfanno.conf
echo 'ops=["max", "max"]' >> vcfanno.conf

#Adding VEST
printf "\n" >> vcfanno.conf
echo '[[annotation]]' >> vcfanno.conf
echo 'file="'$DIR'/vest_precompute_all.bed.gz"' >> vcfanno.conf
echo 'columns=[6]' >> vcfanno.conf
echo 'names=["vest_score"]' >> vcfanno.conf
echo 'ops=["max"]' >> vcfanno.conf
