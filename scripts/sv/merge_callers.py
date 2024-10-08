import sys
import gzip

with gzip.open(sys.argv[1], 'rt') as f:
    for line in f:
        if line[0] == "#":
            if "CHROM" in line:
                 row_list = line.rstrip().split("\t")
                 print("\t".join(row_list[:10]))
            else:
                 print(line.rstrip())
        else:
            row_list = line.rstrip().split("\t")
            GTs = list(set([x for x in row_list[9:] if x != "./."]))
            if len(GTs) == 1:
                GT = GTs
            else:
                GT = ["0/1"]
            print("\t".join(row_list[:9] + GT))
