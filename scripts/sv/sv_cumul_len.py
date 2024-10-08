import sys
import gzip
from collections import OrderedDict

def merge_intervals(intervals):
    # https://stackoverflow.com/questions/43600878/merging-overlapping-intervals/43600953
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals:
        previous = merged[-1]
        if current[0] <= previous[1]:
            previous[1] = max(previous[1], current[1])
            #merged[-1][1] = max(previous[1], current[1])
        else:
            merged.append(current)
    return merged

sam_lst = []
with open(sys.argv[1], 'r') as f:
    for s in f:
        s = s.rstrip()
        sam_lst.append(s)

sv_ids_per_sam = {}
sv_cor = {}
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
            length = abs(int(info['SVLEN']))
            geno = row_list[9:]
            d = dict(zip(samples, geno))
            for x in d:
                y = d[x]
                if y != "./.":
                    sv_ids_per_sam.setdefault(x, []).append(id) 
                    sv_cor[id] = [row_list[0], int(row_list[1]), int(row_list[1]) + length]

sam_counts = OrderedDict()
with open(sys.argv[1], 'r') as f:
    for s in f:
        s = s.rstrip()
        sam_counts[s] = {}

sam_counts = OrderedDict()
check_lst = set()
for i in sam_lst:
    for j in sv_ids_per_sam[i]:
        if j not in check_lst:
            sam_counts.setdefault(i, []).append(sv_cor[j])
            check_lst.add(j)

size = 0
for i in sam_counts:
    temp = {}
    m = 0
    for j in sam_counts[i]:
        chr, start, end = j
        temp.setdefault(chr, []).append([start, end])
    for chr in temp:
        merged_reg = merge_intervals(temp[chr])
        m = sum([x[1] - x[0] + 1 for x in merged_reg])
        size += m
    print i, size
