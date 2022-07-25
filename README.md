# Site-specific chemical similarity
Tool for visualizing the chemical similarity for a given materials system at each unique atomic site.

## Requirements
To run the script, Python 3.7 and the following packages are needed.
- scipy
- pandas
- seaborn
- matplotlib
- pymatgen

## Inputs
The input to the script is data file <em>data.csv</em>, which contains two columns:
1. `formula` - chemical formulae of compounds
2. `property` - materials property values

## Outputs
Heatmaps representing site-specific chemical similarities at each atomic site, with red regions indicating high similarity and blue regions indicating low similarity.

## Usage

```
python calc_similarity.py --site A_B_3
```

Where the argument after flag `--site` is the underscore(\_) separated string of the names of all unique sites. For example, `A_B_X` for perovskites and `X_Y_Z` and `X_2_Y_Z` for half/full heuslers.

## Example
An example <em>data.csv</em> file is provided with the script, which contains the chemical formulae and convex hull energies of compounds with <em>D0_3</em> prototype.