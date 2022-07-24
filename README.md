# Site-specific chemical similarity
Tool for visualizing site-specific chemical similarity for a given materials system.
The output are heatmaps for each atomic site, where red indicates high similarity and blue indicates low similarity.


## Requirements
- scipy
- pandas
- seaborn
- matplotlib
- pymatgen

<em>data.csv</em> is the only file needed and should be placed in the same directory as the script. It should contain the following two columns:
1. `formula` - chemical formulae of compounds
2. `property` - materials property of interest

## Usage


```
python calculate_chemical_similarity.py --data data.csv --site_names A_B_X
```

1. `--data`, name of <em>.csv</em> file

2. `--site_names`, underscore(\_) separated string for the names of all unique sites. (e.g. `A_B_X` for perovskites and `X_Y_Z` for half/full heuslers.)

Note: The current version of code only works when the materials property values are present for **all** elemental combinations.
