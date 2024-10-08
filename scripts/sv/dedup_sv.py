import sys
import gzip
from collections import OrderedDict
import random

vcf = sys.argv[1]
aDict = OrderedDict()

with gzip.open(vcf, 'rt') as f:
    for line in f:
        row_list = line.split()
        if row_list[0][0] == '#':
            print(line.rstrip("\n"))
        else:
            aDict.setdefault(tuple(row_list[:9]), []).append(row_list[9:])

lines = OrderedDict()
for i in aDict:
    if len(aDict[i]) == 1:
        #print("\t".join(list(i) + aDict[i][0]))
        lines.setdefault(list(i)[2], []).append(list(i) + aDict[i][0])
    else:
        # 0/1, 1/1, ./.
        tmp = [list(set(x)) for x in zip(*aDict[i])]
        GT = []
        for t in tmp:
            if len(t) > 1:
                if '0/1' in t:
                    GT.append('0/1')
                else:
                    GT.append('1/1')
            else:
                GT.append(t[0])
        #print("\t".join(list(i) + GT))
        lines.setdefault(list(i)[2], []).append(list(i) + GT)

for i in lines:
    if len(lines[i]) == 1:
        print("\t".join(lines[i][0]))
    else:
        print("\t".join(random.choice(lines[i])))

