bgzip -dc $1.vcf.gz > $1.vcf
SURVIVOR filter $1.vcf NA -1 1000000 0 -1 $1.filtered.vcf
bgzip $1.filtered.vcf
tabix $1.filtered.vcf.gz
rm $1.vcf

