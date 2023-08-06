# abmatrix

[![Upload Python Package](https://github.com/wisdomhealth-inc/abmatrix/actions/workflows/python-publish.yml/badge.svg)](https://github.com/wisdomhealth-inc/abmatrix/actions/workflows/python-publish.yml)

Python3 module defining a class called `abmatrix` to read and parse AB Matrix files

## Module contents

abmatrix.**abmatrix**()

Initialize instance of AB Matrix data set

---

abmatrix.abmatrix.**read**(abmatrixfile)

Read an AB Matrix file, read header and lazy load genotype data

---

abmatrix.abmatrix.**write**(abmatrixfile, genotypes)

Write an AB Matrix file from in-memory instance of class

---

abmatrix.abmatrix.**subset**(locus_list, samples=sample_list)

Get subset of AB Matrix data set. Returns genotype matrix as list
of dictionaries.

---

abmatrix.abmatrix.**close**()

Close instance of abmatrix data set

---

## Example
```python
from abmatrix import abmatrix

# Initialize
myabmatrix = abmatrix.abmatrix()

myabmatrix.read("test_abmatrix.zip")

SNP_IDS = [
    "442_HPS3",
    "054_FGF4_chr12",
    "077_TYRP_LH",
    "077_TYRP1_SH",
    "441_USH2A_roan",
    "277_MC1R_cockersable_Eh",
]

genotypes = myabmatrix.subset(SNP_IDS)
myabmatrix.write("test_abmatrix_subset.ab", genotypes)

myabmatrix.close()
```
