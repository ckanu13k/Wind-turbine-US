#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from sklearn.decomposition import PCA

def model_eval(df, pca_df, pca, k_means_class, k_mbk_class, Lat, Long, year, Num_col):
   
    if len(df) == len(pca_df):
       df['Kmean_class'] = pd.Series(k_means_class, index=df.index)
       df['Kmean_mini_class'] = pd.Series(k_mbk_class, index=df.index)
    else: 
       "the original data to not comform to the data used to generate the model, DANGER!!!"

    ### Check the distribution of the classes generated
    fig, ax = plt.subplots(1,3, figsize=(20, 5))
    for i in range(3):
       tmp = df[df['Kmean_class'] == i]
       tmp['Site.State'].value_counts().plot(kind='bar', ax=ax[i])
    fig.tight_layout()
    plt.savefig('Kmean_class_State.png')

    fig, ax = plt.subplots(1,3, figsize=(20, 5))
    for i in range(3):
       tmp = df[df['Kmean_mini_class'] == i]
       tmp['Site.State'].value_counts().plot(kind='bar', ax=ax[i])
    fig.tight_layout()
    plt.savefig('Kmean_mini_class_State.png')

    ### Map the wind locations based on the classes generated
    fig, ax = plt.subplots(1,3, figsize=(20, 5))
    plt.title('Kmean_class')
    for i in range(3):
       tmp = df[df['Kmean_class'] == i]
       get_map(tmp, ax[i], 'grey', Lat, Long)
    fig.tight_layout()
    plt.savefig('Map_windturbine_locations_Kmean_class.png')

    fig, ax = plt.subplots(1,3, figsize=(20, 5))
    plt.title('Kmean_mini_class')
    for i in range(3):
       tmp = df[df['Kmean_mini_class'] == i]
       get_map(tmp, ax[i], 'grey', Lat, Long)
    fig.tight_layout()
    plt.savefig('Map_windturbine_locations_Kmean_mini_class.png')

    ### Map the wind locations based on the years
    list_year = sorted(df[year].unique())
    fig, ax = plt.subplots(7,5, figsize=(70, 50))
    plt.title('Kmean_mini_class')
    m = 0
    color_list = ['yellow', 'grey', 'red']
    for i in range(7):
       for j in range(5):
          datatmp = df[df[year] == list_year[m]]
          for iclass in range(3):
             get_map(datatmp[datatmp['Kmean_mini_class'] == iclass], ax[i,j], color_list[iclass], Lat, Long)        
             ax[i,j].set_title(list_year[m])
          m+=1
    fig.tight_layout()
    plt.savefig('Map_windturbine_locations_Kmean_mini_class_peryear.png')

    fig, ax = plt.subplots(7,5, figsize=(70, 50))
    plt.title('Kmean_class')
    m = 0
    color_list = ['yellow', 'red', 'grey']
    for i in range(7):
       for j in range(5):
          datatmp = df[df[year] == list_year[m]]
          for iclass in range(3):
             get_map(datatmp[datatmp['Kmean_class'] == iclass], ax[i,j], color_list[iclass], Lat, Long)
             ax[i,j].set_title(list_year[m])
          m+=1
    fig.tight_layout()
    plt.savefig('Map_windturbine_locations_Kmean_class_peryear.png')

    ### Check the highest contributing feature to each principle components
    # number of components
    #print(len(df['Kmean_class'].unique()))
    #pca = PCA(n_components=5)
    n_pcs= pca.components_.shape[0]

    # get the index of the most important feature on EACH component
    # LIST COMPREHENSION HERE
    most_important = [np.abs(pca.components_[i]).argmax() for i in range(n_pcs)]

    initial_feature_names = df.columns.tolist() #['a','b','c','d','e']
    # get the names
    most_important_names = [initial_feature_names[most_important[i]] for i in range(n_pcs)]

    # LIST COMPREHENSION HERE AGAIN
    dic = {'PC{}'.format(i): most_important_names[i] for i in range(n_pcs)}

    # build the dataframe
    df_mp = pd.DataFrame(dic.items())
    print(df_mp)

    ###### Figures
    for col in Num_col:
        fig, ax = plt.subplots(1, 2, figsize=(20, 5))
        for i in range(3):
           tmp = df[df['Kmean_class'] == i]
           tmp[col].plot.hist(bins=10, ax=ax[0], alpha=0.4)
           ax[0].set_xlabel(col)
        for i in range(3):
           tmp = df[df['Kmean_mini_class'] == i]
           tmp[col].plot.hist(bins=10, ax=ax[1], alpha=0.4)
           ax[1].set_xlabel(col)
        fig.tight_layout()
        plt.savefig('Map_windturbine_class_peryear_{}.png'.format(col))

    plt.show()

def get_map(data, axt, color, Lat, Long):
    geometry = [Point(xy) for xy in zip(data[Lat], data[Long])] # There is a problem with the Lat and Long?
    gdf = GeoDataFrame(data, geometry=geometry)   

    #this is a simple map that goes with geopandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    gdf.plot(ax=world.plot(figsize=(20, 12), alpha=0.5, ax=axt, color='silver'), marker='o', color=color, markersize=15);
    axt.set_xlim([-180, 0])
    axt.set_ylim([0, 80])


