# Site-specific chemical similarity
Tool for the calculation and visualization of chemical similarity metrices of elements for a given materials system at each unique atomic site. The resulting similarity matrices may serve as a basis for prototype-substitution method based materials discovery.

## Requirements
Python3.7 with the following packages need to be installed.
- scipy
- pandas
- seaborn
- matplotlib
- pymatgen

## Inputs
<em>data.csv</em>, which contains two columns:
1. `formula` - the chemical formulae of compounds
2. `property` - values for targeted materials property

Both `formula` and `property` columns should contain values for *all* elemental combinations, which could be obtained from exhaustic HT-DFT calculations or ML predictions. Missing values may result in incorrect results.

## Outputs
Running the script will generate two folders:
1. `df_sim` - similarity matrices for elements at each atomic site with rows and columns ordered by increasing Mendeleev number
2. `heatmaps` - heatmaps of similarity matrices of elements at each atomic site. Red regions indicate high similarity, blue regions indicate low similarity.

## Usage

```
python calc_similarity.py --site M1_M2_A_X
```

The argument `M1_M2_A_X` after flag `--site` should be underscore(\_) separated string of including the site names of all unique sites, and should be changed accordingly. For example, `A_B_X` for perovskites and `X_Y_Z` for full heuslers.

## Example Dataset
<em>data.csv</em> contains the chemical formulae and convex hull energies of in-plane ordered MAX phases (i-MAX phases).

## Contact
Ruijie Zhu

Department of Materials Science and Engineering, Northwestern University

ruijiezhu2021@u.northwestern.edu
