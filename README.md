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
python calc_similarity.py --site M1_M2_A_X
```

The argument `M1_M2_A_X` after flag `--site` should be underscore(\_) separated string of the names of all unique sites, and should be changed accordingly. For example, `A_B_X_3` for perovskites and `X_Y_Z` / `X_2_Y_Z` for half/full heuslers.

## Example Dataset
<em>data.csv</em> contains chemical formulae and convex hull energies of i-MAX phases (in-plane ordered MAX phases).

## Contact
Ruijie Zhu
Department of Materials Science and Engineering, Northwestern University
ruijiezhu2021@u.northwestern.edu
