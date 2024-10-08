import sys
from collections import OrderedDict

# HDR stands for Highly Diverged Regions.
# So, HDR are basically regions that are 'different' (not aligned) within a structural unit (syntenic/SR blocks).

syri = sys.argv[1]

inv = open(sys.argv[2], 'w')
trans = open(sys.argv[3], 'w')
pav1 = open(sys.argv[4], 'w') # rearrangements
pav2 = open(sys.argv[5], 'w') # sequence variants
syn =  open(sys.argv[6], 'w')

with open(sys.argv[1], 'r') if sys.argv[1] != "-" else sys.stdin as f:
    for line in f:
        chr, start, end, seq1, seq2, qchr, qstart, qend, svid, svid_p, type, copy_status = line.rstrip().split("\t")
        if type == "INV":
             inv.write("\t".join([chr, start, end, "INV"]) + "\n")
        elif type in ["TRANS", "INVTR"]:
             trans.write("\t".join([chr, start, end, "TRANS"]) + "\n")
        elif type in ["DUP", "INVDP"]:
             if copy_status == "copyloss":
                 pav1.write("\t".join([chr, start, end, "PAV"]) + "\n")
        elif type == "NOTAL" and chr != "-":
             pav1.write("\t".join([chr, start, end, "PAV"]) + "\n")
        elif type in ["CPL","DEL", "HDR", "TDM"]:
             pav2.write("\t".join([chr, start, end, "PAV"]) + "\n")
        elif type == "SYN":
             syn.write("\t".join([chr, start, end, "SYN"]) + "\n")


inv.close()
trans.close()
pav1.close()
pav2.close()
syn.close()

