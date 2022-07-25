import re
import argparse
import itertools
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from pymatgen.core import Element
from scipy import spatial
from xgboost import XGBRegressor
from matminer.featurizers.composition import ElementProperty
from pymatgen.core import Composition
from matminer.featurizers.composition.element import ElementFraction


if __name__ == '__main__':
      
      # load parser
      parser = argparse.ArgumentParser()
      parser.add_argument('--site',help='name of all unique sites along with stoichiometry, separated by underscores')
      args = parser.parse_args()
      
      # load data
      data = pd.read_csv('data.csv')

      # drop duplicates
      data = data.sort_values(by=data.columns[1], ascending=True)
      data = data.drop_duplicates(subset=data.columns[0], keep="first")

      sites_stoi = args.site.split('_')
      sites = [i for i in sites_stoi if not str(i).isdigit()]
      sites_loc = [sites_stoi.index(i) for i in sites]
      stoi = []
      for i in sites_loc:
            if not str(sites_stoi[i+1]).isdigit():
                  stoi.append(1)
            else:
                  stoi.append(int(sites_stoi[i+1]))
      # append site-specific column
      eles = [re.findall('[A-Z][a-z]*',i) for i in data.formula]

      n_sites = len(sites)
      if n_sites != len(eles[0]):
            ValueError('Wrong number of elements specified!')
      eles_df = pd.DataFrame(eles,columns=[f'site_{sites[i]}' for i in range(n_sites)])
      data = data.join(eles_df)
      
      # sort unique elements by mendeleev number (ascending)
      unique_eles = [list(data[f'site_{sites[i]}'].unique()) for i in range(n_sites)]
      unique_eles_sorted = []
      for e in unique_eles:
            mn = [Element[i].mendeleev_no for i in e]
            sorted_ele = list(pd.DataFrame({'ele':e,'mn':mn}).sort_values('mn').ele)
            unique_eles_sorted.append(sorted_ele)

      # df_all_combinations
      all_comb = list(itertools.product(*unique_eles_sorted))
      all_comb_sites = pd.DataFrame(list(zip(*all_comb))).T
      list_all_comb = []
      for i in range(len(all_comb_sites)):
            line = all_comb_sites.iloc[i,:]
            list_all_comb.append(''.join([str(a) + str(b) for a,b in zip(list(line),stoi)]))
      df_all_comb = pd.DataFrame(list_all_comb,columns=['formula'])

      # append site-specific column
      eles = [re.findall('[A-Z][a-z]*',i) for i in df_all_comb.formula]
      eles_df = pd.DataFrame(eles,columns=[f'site_{sites[i]}' for i in range(n_sites)])
      df_all_comb = df_all_comb.join(eles_df)

      ### Use XGBoost to predict property values
      # featurization
      def featurizer(data):
            # Elemental Fraction
            ef = ElementFraction()
            comp_formula = [Composition(i) for i in data.iloc[:,0]]
            data['composition']=comp_formula
            data = ef.featurize_dataframe(data, "composition")
            data = data.loc[:, (data != 0).any(axis=0)] # remove excessive element columns
            # Magpie Features
            ep_feat = ElementProperty.from_preset(preset_name="magpie")
            data = ep_feat.featurize_dataframe(data, col_id="composition")
            # Site Spcific Features
            for e in sites:
                  data[f'mn_{e}'] = [Element(i).mendeleev_no for i in data[f'site_{e}']]
                  data[f'row_{e}'] = [Element(i).row for i in data[f'site_{e}']]
                  data[f'col_{e}'] = [Element(i).group for i in data[f'site_{e}']]
                  data[f'ra_{e}'] = [Element(i).atomic_radius for i in data[f'site_{e}']]
            return data
      
      # featurize dataframe based on the formula column
      len_exist_col = len(data.columns)
      print('Featurizing the training set ...')
      data = featurizer(data)
      data.to_csv('featurized_train.csv',index=False)
      X = data.iloc[:,len_exist_col+1:]
      y = data.iloc[:,1]

      # model training
      xgb = XGBRegressor()
      xgb.fit(X,y)

      # making predictions on all combinations
      len_exist_col = len(df_all_comb.columns)
      print('Featurizing all combinations ...')
      df_all_comb = featurizer(df_all_comb)
      df_all_comb.to_csv('featurized_all_comb.csv',index=False)
      X = df_all_comb.iloc[:,len_exist_col+1:]
      pred = xgb.predict(X)
      df_all_comb['property'] = pred

      # calculate chemical similarities
      for i in range(n_sites):
            prop_matrix=[]
            for s in unique_eles[i]:
                  prop_list = list(df_all_comb[df_all_comb.iloc[:,i]==s].property)
                  prop_matrix.append(prop_list)

            # calculate similarity using cosine distance
            similarity_2d = []
            for j in range(len(prop_matrix)):
                  similarity_1d = []
                  for k in range(len(prop_matrix)):
                        similarity_1d.append(1 - spatial.distance.cosine(prop_matrix[j], prop_matrix[k]))
                  similarity_2d.append(similarity_1d)
            df_sim = pd.DataFrame(similarity_2d,columns=unique_eles[i],index=unique_eles[i])
            
            # output similarity heatmap
            ele_mn = [Element(i).mendeleev_no for i in list(df_sim.index)]
            ele_mn_df = pd.DataFrame({'ele':df_sim.index,'mn':ele_mn})
            sorted_ele = ele_mn_df.sort_values('mn',ascending=True).ele
            sorted_ele_inv = ele_mn_df.sort_values('mn',ascending=False).ele
            df_sim = df_sim.reindex(list(sorted_ele_inv),axis=0)
            df_sim = df_sim.reindex(list(sorted_ele),axis=1)
            plt.figure()
            sns.heatmap(df_sim,cmap='coolwarm',cbar_kws={'label': 'Chemical Similarity'})
            plt.savefig(f'site_{sites[i]}.jpg',dpi=300,bbox_inches = "tight")