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

abmatrix.abmatrix.**write**(abmatrixfile)

Write an AB Matrix file from in-memory instance of class

---

abmatrix.abmatrix.**subset**(locus_list, sample_list)

Get subset of AB Matrix data set

---

abmatrix.abmatrix.**close**()

Close instance of abmatrix data set

---

## Example
```python
from abmatrix import abmatrix

# Initialize
myabmatrix = abmatrix.abmatrix()

myabmatrix.open("test_abmatrix.zip")

TRAIT_LIST = [
    "442_HPS3",
    "054_FGF4_chr12",
    "077_TYRP_LH",
    "077_TYRP1_SH",
    "441_USH2A_roan",
    "277_MC1R_cockersable_Eh",
]

output = myabmatrix.reduce(TRAIT_LIST)
print(output)

myabmatrix.close()
```
