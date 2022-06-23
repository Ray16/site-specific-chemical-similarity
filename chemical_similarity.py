import re
import argparse
import itertools
from scipy import spatial
import pandas as pd
import seaborn as sns
from pymatgen.core import Element
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--data',help='specify the name of data files (.csv)')
parser.add_argument('--site_names',help='specify the name of all unique sites, separated by underscore "_"')
args = parser.parse_args()

data = pd.read_csv(args.data)
site_names = args.site_names.split('_')
eles = [re.findall('[A-Z][a-z]*',i) for i in data.formula]

n_sites = len(eles[0])

for i in range(n_sites):
      data[f'site_{site_names[i]}.jpg'] = list(zip(*eles))[i]

# sort unique elements by mendeleev number
unique_ele = [list(pd.DataFrame(eles).iloc[:,i].unique()) for i in range(n_sites)]
unique_ele_sorted = []
for u_e in unique_ele:
      mn = [Element[i].mendeleev_no for i in u_e]
      sorted_ele = list(pd.DataFrame({'ele':u_e,'mn':mn}).sort_values('mn').ele)
      unique_ele_sorted.append(sorted_ele)

# df_all_combinations
all_combinations = list(itertools.product(*unique_ele_sorted))
df_all_combinations = pd.DataFrame(list(zip(*all_combinations))).T
df_all_combinations.columns = data.columns[2:]
# append Ehull (rename to df_found)
df_found = pd.merge(df_all_combinations, data.iloc[:, 1:], how='inner')
df_found = df_found.merge(df_all_combinations)

# calculate chemical similarities
for i in range(n_sites):
      Ehull_matrix=[]
      for s in unique_ele[i]:
            Ehull_list = list(df_found[df_found.iloc[:,i]==s].Ehull)
            Ehull_matrix.append(Ehull_list)

      # calculate similarity using cosine distance
      similarity_2d = []
      for j in range(len(Ehull_matrix)):
            similarity_1d = []
            for k in range(len(Ehull_matrix)):
                  similarity_1d.append(1 - spatial.distance.cosine(Ehull_matrix[j], Ehull_matrix[k]))
            similarity_2d.append(similarity_1d)
      df_sim = pd.DataFrame(similarity_2d,columns=unique_ele[i],index=unique_ele[i])
      
      # output similarity heatmap
      ele_mn = [Element(i).mendeleev_no for i in list(df_sim.index)]
      ele_mn_df = pd.DataFrame({'ele':df_sim.index,'mn':ele_mn})
      sorted_ele = ele_mn_df.sort_values('mn',ascending=True).ele
      sorted_ele_inv = ele_mn_df.sort_values('mn',ascending=False).ele
      df_sim = df_sim.reindex(list(sorted_ele_inv),axis=0)
      df_sim = df_sim.reindex(list(sorted_ele),axis=1)
      plt.figure()
      sns.heatmap(df_sim,cmap='coolwarm',cbar_kws={'label': 'Chemical Similarity'})
      plt.savefig(f'site_{site_names[i]}.jpg',dpi=300,bbox_inches = "tight")
