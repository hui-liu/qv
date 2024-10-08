# $1: ref
# $2: hifi reads
# $3: sample
# $4: tandem repeat

minimap2 --MD -ax map-hifi --eqx --cs \
$1 \
$2 | \
samtools view -@ 48 -bS | \
samtools sort -@ 48 -o $3.bam

samtools index $3.bam
