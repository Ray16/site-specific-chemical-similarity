# Site-specific chemical similarity
Visualization of site-specific chemical similarity for a given materials system.

## Requirements
- scipy
- pandas
- seaborn
- matplotlib
- pymatgen

The <em>data.csv</em> file is needed, which contains two columns:
1. `formula`, chemical formulae of compounds
2. `property`, the materials property of interest

## Usage

```
python calculate_chemical_similarity.py --data data.csv --site_names A_B_X
```

The example code above takes in <em>data.csv</em> as input and outputs the chemical similarity heatmaps for each unique site.

The two arguments are needed to be specified:

1. `--data`, name of <em>.csv</em> file

2. `--site_names`, underscore(\_) separated string for the names of all unique sites. (e.g. `A_B_X` for perovskites and `X_Y_Z` for half/full heuslers.)

Note: The current version of code only works when the materials property values are present for **all** elemental combinations.
