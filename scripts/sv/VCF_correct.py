import sys
import gzip

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
    seq = reference[(start-1):end]
    if strand == "-":
        seq = reverse_comp(seq)
    return seq

ref = sys.argv[1]
vcf = sys.argv[2]

ref_dict = parseFasta(ref)
n = 0
info_added = False
with gzip.open(vcf, 'rt') as f:
    for line in f:
        if line[0] == '#':
            if '##fileformat' in line or '##contig' in line:
                print(line.rstrip("\n"))
            elif '#CHROM' in line:
                row_list = line.split()
                print("\t".join(row_list))
            else:
                continue
        if not info_added:
            print('##INFO=<ID=ID,Number=A,Type=String,Description="IDs of the original variants">')
            print('##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variation">')
            print('##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Length of structural variation">')
            print('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">')
            info_added = True
        row_list = line.split()
        if row_list[0][0] != '#':
            if "IMPRECISE" in row_list[7]:
                continue
            d = dict([i.split("=") for i in row_list[7].split(";") if "=" in i])
            if d["SVTYPE"] == "BND": continue
            #if d["SVTYPE"] == "INV" and "SVLEN" not in d:
            #    row_list[7] = row_list[7].replace("SUPPORT", "SVLEN=" + str(len(row_list[3])) +";SUPPORT")
            #    d = dict([i.split("=") for i in row_list[7].split(";") if "=" in i])
            sv_len =  abs(int(d["SVLEN"]))
            if sv_len > 100000 or sv_len < 50: continue
            chr, start, end = row_list[0], int(row_list[1]), int(row_list[1]) + abs(int(d["SVLEN"]))
            seq = getSeq([chr, start, end, "+"], ref_dict[chr])
            id = "sv_" + chr + "_" + str(start)
            row_list[5] = "."
            row_list[6] = "."
            row_list[8] = row_list[8].split(":")[0]
            samples = [x.split(":")[0] for x in row_list[9:]]
            row_list = row_list[:9] + samples
            if d["SVTYPE"] == "DEL":
                row_list[3] = seq
                row_list[4] = seq[0]
                if len(row_list[3]) > len(row_list[4]):
                    n += 1
                    row_list[2] = id
                    info = "ID=" + id + ";" + "SVTYPE=DEL;" + "SVLEN=-" + str(sv_len)
                    row_list[7] = info
                    print("\t".join(row_list))
            elif d["SVTYPE"] == "INS":
                row_list[3] = seq[0]
                if len(row_list[3]) < len(row_list[4]):
                    n += 1
                    row_list[2] = id
                    info = "ID=" + id + ";" + "SVTYPE=INS;" + "SVLEN=" + str(sv_len)
                    row_list[7] = info
                    print("\t".join(row_list))
            elif d["SVTYPE"] == "INV":
                row_list[3] = seq[0]
                row_list[4] = reverse_comp(seq)
                n += 1
                row_list[2] = id
                info = "ID=" + id + ";" + "SVTYPE=INV;" + "SVLEN=" + str(sv_len)
                row_list[7] = info
                print("\t".join(row_list))
            elif d["SVTYPE"] == "DUP":
                row_list[3] = seq[0]
                row_list[4] = seq
                n += 1
                row_list[2] = id
                info = "ID=" + id + ";" + "SVTYPE=DUP;" + "SVLEN=" + str(sv_len)
                row_list[7] = info
                print("\t".join(row_list))
