# Site-specific Chemical Similarity
This repository contains code for calculating site-specific chemical similarity for any materials system with given materials property.

To properly run the code, the following packages are needed:
- scipy
- pandas
- seaborn
- matplotlib
- pymatgen

The <em>data.csv</em> file should contain the following two columns:
1. `formula`, chemical formulae of compounds
2. `property`, the materials property of interest

## Running the script
The script can be run using one line of code:

```
python calculate_chemical_similarity.py --data data.csv --site_names M1_M2_A_X
```

The example code above takes in <em>data.csv</em> as input and outputs the chemical similarity heatmaps for each unique site.

The two arguments that need to be specified are:

1. `--data`, the name of the <em>.csv</em> file

2. `--site_names`, underscore(\_) separated string for the names of all unique sites. (e.g. `A_B_X` for perovskites and `X_Y_Z` for half/full heuslers.)

Note: The current version of code only works when the materials property values are present for **all** elemental combinations.
