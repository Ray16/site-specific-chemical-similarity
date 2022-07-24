# Site-specific chemical similarity
Tool for visualizing site-specific chemical similarity for a given materials system. 


## Requirements
- scipy
- pandas
- seaborn
- matplotlib
- pymatgen

## Input
<em>data.csv</em> is the only file needed and should be placed in the same directory as the script. It should contain the following two columns:
1. `formula` - chemical formulae of compounds
2. `property` - materials property values

## Output
Heatmaps representing site-specific chemical similarities for each atomic site. Red regions indicate high similarity and blue regions indicate low similarity.

## Usage

```
python calculate_chemical_similarity.py --data data.csv --site_names A_B_X
```

1. `--data` - name of <em>.csv</em> file

2. `--site_names` - underscore(\_) separated string of the names of all unique sites. (e.g. `A_B_X` for perovskites and `X_Y_Z` for half/full heuslers.)
