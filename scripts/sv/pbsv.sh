# $1: ref
# $2: bam
# $3: tandem repeat
# $4: sample

source ~/.bash_conda
conda activate pbsv

for i in $(samtools view -H $2 | grep '^@SQ' | cut -f2 | cut -d':' -f2); do
pbsv discover \
--region $i \
--hifi \
--min-mapq 20 \
--min-svsig-length 50 \
--tandem-repeats $3 \
$2 $4.$i.svsig.gz
done

pbsv call \
-j 12 \
--hifi \
--preserve-non-acgt \
-t DEL,INS,INV,DUP,BND \
-m 50 \
--log-level INFO \
$1 \
$4.Chr1.svsig.gz \
$4.Chr2.svsig.gz \
$4.Chr3.svsig.gz \
$4.Chr4.svsig.gz \
$4.Chr5.svsig.gz \
$4.Chr6.svsig.gz \
$4.Chr7.svsig.gz \
$4.Chr8.svsig.gz \
$4.Chr9.svsig.gz \
$4.Chr10.svsig.gz \
$4.Chr11.svsig.gz \
$4.Chr12.svsig.gz \
$4.vcf

#pbsv discover \
#--hifi \
#--min-mapq 20 \
#--min-svsig-length 50 \
#--tandem-repeats $3 \
#$2 $4.svsig.gz

#pbsv call \
#--hifi \
#--preserve-non-acgt \
#-t DEL,INS,INV,DUP,BND \
#-m 50 \
#$1 $4.svsig.gz $4.vcf

bgzip $4.vcf
tabix $4.vcf.gz
