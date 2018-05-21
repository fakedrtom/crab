#Get the latest CIViC files
echo "Retrieving the latest data from DoCM"
curl -o docm.tsv -L http://www.docm.info/api/v1/variants.tsv?versions=3.2

echo "Preparing BED file"
python make_docm_bed.py > docm.bed

