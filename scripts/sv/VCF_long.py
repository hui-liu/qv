import sys
import gzip

vcf = sys.argv[1]

with gzip.open(vcf, 'rt') as f:
    for line in f:
        if line[0] == '#':
            print(line.rstrip("\n"))
        else:
            row_list = line.split()
            d = dict([i.split("=") for i in row_list[7].split(";") if "=" in i])
            sv_len = abs(int(d["SVLEN"]))
            if sv_len > 100000:
                print("\t".join(row_list))
