# $1: sample
# $2: ref
source ~/.bash_conda
conda activate svimasm_env

svim-asm haploid --query_names --interspersed_duplications_as_insertions \
--min_sv_size 50 --max_sv_size 10000000 \
--sample $1 results $1.bam $2

