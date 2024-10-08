# $1: bam
# $2: ref
# $3: sample

source ~/.bash_conda
conda activate cuteSV

cuteSV \
$1 \
$2 \
$3.vcf \
./ \
--sample $3 \
--min_support 4 \
--min_mapq 20 \
--min_size 50 \
--genotype \
--threads 48 \
--max_cluster_bias_INS 1000 \
--diff_ratio_merging_INS 0.9 \
--max_cluster_bias_DEL 1000 \
--diff_ratio_merging_DEL 0.5

bgzip $3.vcf

