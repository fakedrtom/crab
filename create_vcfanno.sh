#Create a vcfanno.conf file
DIR=`pwd`

#Adding CIViC
echo '[[annotation]]' > vcfanno.conf
echo 'file="'$DIR'/civic/civic_genes_summaries.bed.gz"' >> vcfanno.conf
echo 'columns=[4,5,6,7,8,9,10,11,12,13,14,15,16]' >> vcfanno.conf
echo 'names=["civic_gene","civic_gene_n_vars","civic_gene_var_ids","civic_gene_n_evis","civic_gene_evi_ids","civic_gene_max_level","civic_gene_max_rating","civic_gene_evi_types","civic_gene_evi_directions","civic_gene_clin_sigs","civic_gene_origins","civic_gene_diseases","civic_gene_max_score"]' >> vcfanno.conf
echo 'ops=["self","max","self","max","self","self","max","self","self","self","self","self","max"]' >> vcfanno.conf
printf "\n" >> vcfanno.conf
echo '[[annotation]]' >> vcfanno.conf
echo 'file="'$DIR'/civic/civic_variants.bed.gz"' >> vcfanno.conf
echo 'columns=[6,6,8,9,10,11,12,13,14,15,16]' >> vcfanno.conf
echo 'names=["in_civic","civic_var_id","civic_score", "civic_evi_type","civic_evi_level","civic_evi_direction","civic_clin_sig","civic_rating","civic_evi_id","civic_var_origin","civic_disease"]' >> vcfanno.conf
echo 'ops=["flag","concat","concat","concat","concat","concat","concat","concat","concat", "concat", "concat"]' >> vcfanno.conf

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
echo 'file="'$DIR'/docm/docm.bed"' >> vcfanno.conf
echo 'columns=[6,6,7,8,9]' >> vcfanno.conf
echo 'names=["in_docm","docm_gene","docm_mutation_type","docm_disease","docm_pubmed"]' >> vcfanno.conf
echo 'ops=["flag","self","self","self","self"]' >> vcfanno.conf

