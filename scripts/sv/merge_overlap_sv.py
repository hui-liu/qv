import sys
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


input = sys.argv[1]
svtype = sys.argv[2]
out = open(sys.argv[3], 'w')

sv = OrderedDict()
with open(input, 'r') as f:
    for line in f:
        chr,start,end,type = line.rstrip().split("\t")
        sv.setdefault(chr, []).append([int(start), int(end)])


for chr in sv:
    merged_reg = merge_intervals(sv[chr])
    for x in merged_reg:
        out.write("\t".join([chr] + map(str, x) + [svtype]) + '\n')

out.close()
