# $1: ref
# $2: path to qry file
# $3: sample
source ~/.bash_conda
conda activate syri

minimap2 -x asm5 -a --eqx --cs -t 24 \
$1 $2/$3.chr.fasta | \
samtools sort -O BAM - > $3.bam
samtools index $3.bam
syri -c $3.bam -r $1 -q $2/$3.chr.fasta -k -F B -f --nc 12 --prefix $3_

