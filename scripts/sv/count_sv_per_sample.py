import sys
from collections import OrderedDict
import gzip

counts = OrderedDict()
with open(sys.argv[1], 'r') as f:
    for s in f:
        s = s.rstrip()
        counts[s] = {'INS': 0, 'DEL': 0, 'INV': 0}

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
            info = dict([v.split("=") for v in row_list[7].split(";")])
            svtype = info['SVTYPE']
            geno = row_list[9:]
            d = dict(zip(samples, geno))
            for x in d:
                y = d[x]
                if y != "./.":
                    counts[x][svtype] += 1


for sample in counts:
    for sv in ["INS", "DEL", "INV"]:
        print "\t".join([sample, sv, str(counts[sample][sv])])

