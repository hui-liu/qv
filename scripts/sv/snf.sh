# $1: ref
# $2: bam
# $3: tandem repeat
# $4: sample

source ~/.bash_conda

sniffles \
--reference $1 \
--input $2 \
--tandem-repeats $3 \
--threads 24 \
--minsupport 4 \
--minsvlen 50 \
--vcf $4.vcf.gz \
--snf $4.snf \
--sample-id $4

