# site-specific-chemical-similarity
This repository contains code for calculating site-specific chemical similarity for any materials system with a given materials property.

The following packages are needed for running the code (all can be installed using `pip install`):
- scipy
- pandas
- seaborn
- matplotlib
- pymatgen

The <em>data.csv</em> file should contain the following two columns:
1. `formula`, chemical formulae of compounds
2. `property`, the materials property of interest

## Running the script
The script can be run using just one line of code:

```
python chemical_similarity.py --data data.csv --site_names M1_M2_A_X
```
The example script above takes in <em>data.csv</em> as input and output the chemical similarity heatmaps for unique each site (site_M1, site_M2, site_A and site_X).

The two arguments that need to specified here are:

1. `--data`, the name of the <em>.csv</em> data file

2. `--site_names`, underscore(\_) separated string for names of all unique sites

For example, `A_B_X` for perovskites and `X_Y_Z` for half/full heuslers.

Note: The current version of code only works when the materials properties are present for **all** elemental combinations, i.e. there should be no **NaN** in the `property` column.
