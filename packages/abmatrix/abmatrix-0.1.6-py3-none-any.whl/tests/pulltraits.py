import sys
import csv
from abmatrix import abmatrix


V5_MANIFEST = "Mars_100k_20006795X361749_A1.bpm"
V6_MANIFEST = "Neogen_Canine_100Kv2_20007095X383071_A1.bpm"

V5_TRAIT_LIST = [
    "335_EPAS1",
    "339_LMBR1_DC1",
    "067_T-box_transcription_factor_T",
    "393_ALX4_JPA",
    "339_LMBR1_DC2",
    "362_ACSL4",
    "198_Skull_shape_CFA32_8196098",
    "054_FGF4_insertion_F",
    "193_Ear_morphology_chr10_11072007",
    "195_SMOC2_inspoint1",
    "326C_MC5R",
    "284_SLC45A2_albino_caL",
    "177_FGF5",
    "338_SGK3_SD",
    "140_FOXI3_chr17_37651314",
    "157_Ridge_JPA1",
    "185_RALY_duplication",
    "155_KRT71",
    "338_SGK3",
    "244_FGF5_c556del",
    "244_FGF5_c578_new",
    "244_FGF5_g8193",
    "146_ASIP_recessive_black_new",
    "095_ASIP_black-and-tan_variable_SINE",
    "076_ASIP_yellow-tan_1mutation",
    "077_TYRP1_bs_mutation",
    "077_TYRP1_bc_mutation",
    "077_TYRP1_AS",
    "077_TYRP1_bd_345delP",
    "062_MLPH_d3",
    "062_MLPH_d2",
    "189_MC1R_grizzle_mutation_Eg",
    "080_MC1R_e-locus",
    "081_MC1R_em-locus",
    "080_MC1R_e3_allele",
    "080_MC1R_e2_allele",
    "215_MC1R_ancient",
    "153_PSMB7",
    "428_MFSD12",
    "082_CBD103",
    "094_merle_SINE",
    "093_MITF_SINE",
]

V6_TRAIT_LIST = [
    "442_HPS3",
    "054_FGF4_chr12",
    "077_TYRP_LH",
    "077_TYRP1_SH",
    "441_USH2A_roan",
    "277_MC1R_cockersable_Eh",
]

NOT_FOUND_LIST = [
    "083_RSPO2_consensus",
    "244_FGF5_c559dup_consensus",
    "062_MLPH_D1_consensus",
]

# Check for input abmatrix argument
if len(sys.argv) < 2:
    print("Usage: pulltraits.py <abmatrix>")
    sys.exit(1)

filename = sys.argv[1]
myabmatrix = abmatrix()
myabmatrix.open(filename)
if myabmatrix.header["Content"] == V6_MANIFEST:
    trait_list = V5_TRAIT_LIST + V6_TRAIT_LIST
else:
    trait_list = V5_TRAIT_LIST
locuslist = myabmatrix.locus(trait_list)
samplelist = myabmatrix.samplelist()
results = {}

for locus in locuslist:
    locus_array = locus.split("\t")
    locus_name = locus_array.pop(0)
    for i, geno in enumerate(locus_array):
        sampleid = samplelist[i]
        x = "0"
        if geno == "AB":
            x = "1"
        elif geno == "BB":
            x = "2"
        elif geno == "--":
            x = ""
        if sampleid in results:
            results[sampleid][locus_name] = x
        else:
            results[sampleid] = {locus_name: x}
myabmatrix.close()

# Write output CSV file
with open("out.csv", "w") as f:
    fieldnames = ["id"] + trait_list
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for key, val in results.items():
        outdict = {"id": key}
        for key2, val2 in val.items():
            outdict[key2] = val2
        writer.writerow(outdict)
