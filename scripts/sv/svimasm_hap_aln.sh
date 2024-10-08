# $1: ref asm
# $2: qry asm
# $3: sample

minimap2 -x asm5 -a --eqx --cs -t 48 \
$1 \
$2 | \
samtools view -@ 48 -bS | \
samtools sort -@ 48 -o $3.bam
samtools index $3.bam

