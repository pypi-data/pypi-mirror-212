import sys
from abmatrix import abmatrix

SAMPLE_IDS = [
    "BSNRPVD",
    "BCSMXTL",
    "DYVNMCB",
    "PHZJVGW",
    "PWRZSMX",
    "DFMTPVJ",
    "BRTLPZB"
]

SNP_IDS = [
    "442_HPS3",
    "054_FGF4_chr12",
    "077_TYRP_LH",
    "077_TYRP1_SH",
    "441_USH2A_roan",
    "277_MC1R_cockersable_Eh"
]

input_file = sys.argv[1]
output_file = "mytest.ab"
ab = abmatrix.abmatrix()
ab.read(input_file)
ol = ab.subset(SNP_IDS, samples=SAMPLE_IDS)
ab.write(output_file, ol)
ab.close()
