# Site-specific chemical similarity
A tool for visualizing the chemical similarity of a given materials system at each unique atomic site.

## Requirements
To run the scripts, Python3.7 with the following packages need to be installed.
- scipy
- pandas
- seaborn
- matplotlib
- pymatgen

## Inputs
A data file called <em>data.csv</em> is needed, which contains two columns:
1. `formula` - the chemical formulae of compounds
2. `property` - vales for the target materials property

## Outputs
1. `df_sim` - This folder contains similarity matrices with rows and columns ordered by Mendeleev Number
2. `heatmaps` - This folder contains heatmaps representing similarities at each atomic site. Red regions indicate high similarity, blue regions indicate low similarity.

## Usage

```
python calc_similarity.py --site A_B_3
```

The argument after flag `--site` should be underscore(\_) separated string of the names of all unique sites.
For example, `A_B_X` for perovskites and `X_Y_Z` and `X_2_Y_Z` for half/full heuslers.

## Example Data
The example <em>data.csv</em> file contains chemical formulae and convex hull energies of compounds of i-MAX phases (in-plane ordered MAX phases).
