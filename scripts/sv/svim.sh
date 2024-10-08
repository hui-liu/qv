# $1: sample
# $2: bam
# $3: ref

source ~/.bash_conda
conda activate svim_env

svim alignment \
--interspersed_duplications_as_insertions \
--read_names \
--zmws \
--min_sv_size 50 \
--minimum_depth 4 \
--cluster_max_distance 0.5 \
--sample $1 \
$1 \
$2 \
$3

bgzip $1/variants.vcf
