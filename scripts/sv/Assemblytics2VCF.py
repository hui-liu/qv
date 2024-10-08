import sys
import gzip

def LoadVcfHeader():
    Header = '##fileformat=VCFv4.2\n\
##INFO=<ID=ID,Number=A,Type=String,Description="IDs of the original variants">\n\
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variation">\n\
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Length of structural variation">\n\
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n\
##contig=<ID=Chr1,length=55364609>\n\
##contig=<ID=Chr2,length=98039476>\n\
##contig=<ID=Chr3,length=73683396>\n\
##contig=<ID=Chr4,length=90986374>\n\
##contig=<ID=Chr5,length=91417692>\n\
##contig=<ID=Chr6,length=50530958>\n\
##contig=<ID=Chr7,length=45000571>\n\
##contig=<ID=Chr8,length=64811439>\n\
##contig=<ID=Chr9,length=55369506>\n\
##contig=<ID=Chr10,length=56931909>\n\
##contig=<ID=Chr11,length=55436004>\n\
##contig=<ID=Chr12,length=39730782>'
    return Header

def parseFasta(filename):
    fas = {}
    id = None
    with open(filename, 'r') as fh:
        for line in fh:
            if line[0] == '>':
                header = line[1:].rstrip()
                id = header.split()[0]
                fas[id] = []
            else:
                fas[id].append(line.rstrip().upper())
        for id, seq in fas.iteritems():
            fas[id] = ''.join(seq)
    return fas

def reverse_comp(sequence):
    comp_dict = {
        'A': 'T',
        'B': 'V',
        'C': 'G',
        'D': 'H',
        'G': 'C',
        'H': 'D',
        'M': 'K',
        'N': 'N',
        'R': 'Y',
        'S': 'S',
        'T': 'A',
        'U': 'A',
        'V': 'B',
        'W': 'W',
        'X': 'X',
        'Y': 'R'}
    sequence = sequence.upper()
    sequence_rev = ''
    for i in range(1, len(sequence)+1):
        sequence_rev += comp_dict[sequence[-i]]
    return sequence_rev

def getSeq(record, reference):
    chr, start, end, strand = record
    start, end = int(start), int(end)
    seq = reference[(start-1):end]
    if strand == "-":
        seq = reverse_comp(seq)
    return seq

ref = sys.argv[1]
sv_bed = sys.argv[2]
sample_genome = sys.argv[3]
sample = sys.argv[4]


ref_dict = parseFasta(ref)
sam_dict = parseFasta(sample_genome)

VcfHeader = LoadVcfHeader()
VcfHeaderLine = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT'
print(VcfHeader)
print(VcfHeaderLine+"\t"+sample)

with open(sv_bed, 'r') as f:
    for line in f:
        if line[0] == "#":
            continue
        else:
            ref_chr,ref_start,ref_stop,ID,size,strand,type,ref_gap_size,query_gap_size,query_coordinates,method = line.split()
            size = abs(int(size))
            if size <= 50: continue
            ref_seq = getSeq([ref_chr, ref_start, int(ref_start) + size - 1, strand], ref_dict[ref_chr])
            ID= "sv_" + ref_chr + "_" + ref_start
            if type == "Deletion":
                info = "ID=" + ID + ";SVTYPE=DEL" + ";SVLEN=-" + str(size)
                print("\t".join([ref_chr, ref_start, ID, ref_seq, ref_seq[0], ".", ".", info, "GT", "1/1"]))
            elif type == "Insertion":
                qid, qcoor, qstrand = query_coordinates.split(":")
                qstart, qend = qcoor.split("-")
                sam_seq = getSeq([qid, qstart, qend, qstrand], sam_dict[qid])
                alt_seq = ref_seq[0]+sam_seq
                info = "ID=" + ID + ";SVTYPE=INS" + ";SVLEN=" + str(len(alt_seq))
                print("\t".join([ref_chr, ref_start, ID, ref_seq[0], alt_seq, ".", ".", info, "GT", "1/1"]))
