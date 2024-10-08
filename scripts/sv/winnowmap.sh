# $1: ref
# $2: hifi reads
# $3: sample

source ~/.bash_conda
conda activate winnowmap

winnowmap -x map-pb -a -Y -L --eqx --cs \
--MD --secondary=no -t 48 \
-R "@RG\tID:$3\tSM:$3" \
-W /mnt/Data_disk/liuhui/Qvariabilis/SV/winnowmap/SDTS.h1.kmer/repetitive_k15.txt \
$1 \
$2 | \
samtools view -@ 48 -b - > $3.bam
samtools sort -@ 48 $3.bam -o $3_sorted.bam
samtools index $3_sorted.bam
rm $3.bam
