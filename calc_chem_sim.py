import argparse
import pandas as pd
from scipy.spatial import distance
import seaborn as sns
from pymatgen.core import Element
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')
data = data.sort_values('formula')

parser = argparse.ArgumentParser()
parser.add_argument('--site',help='underscore(_) separated site names')
args = parser.parse_args()
all_sites = args.site.split('_')

for i,site in enumerate(all_sites):
      data[site] = [f.split('-')[i] for f in data.formula]


for site in all_sites:
      unique_ele = list(data[site].unique())
      mn_ele = [Element(i).mendeleev_no for i in unique_ele]
      unique_ele = pd.DataFrame({'ele':unique_ele,'mn_ele':mn_ele}).sort_values('mn_ele').ele.values

      ################ similarity site ################
      matrix_Ehull=[] # dim: num of unique elements * num of all elemental combinations containing a given element
      matrix_formula=[] # dim: num of unique elements * num of all elemental combinations containing a given element

      for e in unique_ele:
            list_all_comb_formula = list(data[data[site]==e].formula)
            matrix_formula.append(list_all_comb_formula)
            list_all_comb_prop = list(data[data[site]==e].property)
            matrix_Ehull.append(list_all_comb_prop)

      # calc similarity using cosine distance
      similarity_2d = []
      for i in range(len(matrix_Ehull)):
            ele_i = unique_ele[i]
            Ehull_i_list = matrix_Ehull[i]
            formula_i_list = matrix_formula[i]
            similarity_1d = []
            for j in range(len(matrix_Ehull)): 
                  ele_j = unique_ele[j]

                  Ehull_j_list = matrix_Ehull[j]
                  formula_j_list = matrix_formula[j]
                  # remove
                  # remove compounds containing ele_i in Ehull_j_list -> new_Ehull_j_list
                  new_Ehull_j_list = []
                  new_formula_j_list = []
                  for c,item in enumerate(formula_j_list):
                        if ele_i not in item.split('-'):
                              new_Ehull_j_list.append(Ehull_j_list[c])
                              new_formula_j_list.append(formula_j_list[c])

                  # remove compounds containing ele_j in Ehull_i_list -> new_Ehull_i_list
                  new_Ehull_i_list = []
                  new_formula_i_list = []
                  for c,item in enumerate(formula_i_list):
                        if ele_j not in item.split('-'):
                              new_Ehull_i_list.append(Ehull_i_list[c])
                              new_formula_i_list.append(formula_i_list[c])

                  sim_val = 1 - distance.cosine(new_Ehull_i_list, new_Ehull_j_list)

                  similarity_1d.append(sim_val)
            similarity_2d.append(similarity_1d)
      df_sim = pd.DataFrame(similarity_2d,columns=unique_ele,index=unique_ele)

      # plot similarity heatmap
      ele_mn = [Element(i).mendeleev_no for i in list(df_sim.index)]
      ele_mn_df = pd.DataFrame({'ele':df_sim.index,'mn':ele_mn})
      sorted_ele = ele_mn_df.sort_values('mn',ascending=True).ele
      sorted_ele_inv = ele_mn_df.sort_values('mn',ascending=False).ele
      df_sim = df_sim.reindex(list(sorted_ele_inv),axis=0)
      df_sim = df_sim.reindex(list(sorted_ele),axis=1)
      plt.figure(figsize=(30,20))
      sns.heatmap(df_sim,cmap='coolwarm',cbar_kws={'label': 'Chemical Similarity'})
      plt.savefig(f'heatmaps/sim_{site}.eps',bbox_inches = "tight")
      plt.close()
      df_sim.to_csv(f'df_sim/df_sim_{site}.csv')