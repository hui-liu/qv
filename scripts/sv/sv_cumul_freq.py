import sys
import gzip
from collections import OrderedDict

sam_counts = OrderedDict()
with open(sys.argv[1], 'r') as f:
    for s in f:
        s = s.rstrip()
        sam_counts[s] = 0

sv_ids_per_sam = {}
with gzip.open(sys.argv[2], 'rt') as f:
    for line in f:
        if line[0] == "#":
            if "CHROM" in line:
                row_list = line.rstrip().split("\t")
                samples = row_list[9:]
            else:
                continue
        else:
            row_list = line.rstrip().split("\t")
            id = row_list[2]
            info = dict([v.split("=") for v in row_list[7].split(";")])
            geno = row_list[9:]
            d = dict(zip(samples, geno))
            for x in d:
                y = d[x]
                if y != "./.":
                    sv_ids_per_sam.setdefault(x, []).append(id)

check_lst = set()
for i in sam_counts:
    for j in sv_ids_per_sam[i]:
        if j not in check_lst:
            sam_counts[i] += 1
            check_lst.add(j)

m = 0
for i in sam_counts:
    m += sam_counts[i]
    print i, m
