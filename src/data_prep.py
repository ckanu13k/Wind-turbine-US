#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

import pickle
from geopy.geocoders import Nominatim
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import datetime as dt
import time
from io import BytesIO

import holoviews as hv
from holoviews import dim, opts
hv.notebook_extension('bokeh', width=90)

import seaborn as sns

from sklearn.preprocessing import StandardScaler, RobustScaler, Normalizer
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.decomposition import PCA
from sklearn import metrics
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
#from kmeans_interp.kmeans_feature_imp import KMeansInterp

from outlier_data import outlier_prep
#obj = outlier_prep() #import outlier_aware_hist, outlier_data
np.random.seed(0)


def main(df, Numerical_col, Location_col, Data_col, Cat_col):

    #Plot the numerical features 
    data = df[Numerical_col + Data_col]
    fig, ax = plt.subplots(4, 2, figsize=(20, 18))
    m=0
    for i in range(4):
        for j in range(2):
            if m > len(data.columns):
               pass
            else:
               data_tmp = data[data.columns[m]].dropna()
               obj = outlier_prep(data_tmp,ax[i,j], data.columns[m])
               obj.outlier_aware_hist() #data_tmp,ax[i,j], data.columns[m], *obj.calculate_bounds(data_tmp))  
            m+=1
   
    #Prep category data
    data_cat = df[Cat_col]
    data_cat = data_cat.dropna()

    list_4_bin = []
    for col in Cat_col:
        if len(data_cat[col].unique()) < 45:
           list_4_bin.append(col)
    
    df = convert_categorical(df,list_4_bin)
    FLAGS = diff(Cat_col, list_4_bin)
    CATEGORICAL_FEATURES = {}
    for ilist in list_4_bin:
        CATEGORICAL_FEATURES[ilist] = range(len(data_cat[ilist].unique()))

    #print(df.head, FLAGS, Data_col, CATEGORICAL_FEATURES)
    df_cln = cat_encode(df.drop(FLAGS,axis=1), CATEGORICAL_FEATURES)
    #print(df_cln)
    ## Drop the year - it seems irrelevant
    df_cln = df_cln.drop(Data_col,axis=1)

    ### Normalize the data for ML analysis
    df_scal, scal_mean, scal_var = dnorm(df_cln)

    pca = PCA(n_components=5)
    principalComponents = pca.fit_transform(df_scal)
    principalDf = pd.DataFrame(data = principalComponents, columns = ['p1', 'p2', 'p3', 'p4', 'p5'])
    return principalDf, pca



### Normalize the data for ML analysis
def dnorm(df):
    df_out = df
    temp = df.filter(regex='~')
    dum_col = temp.columns.tolist()
    X_undum = df.drop(dum_col, axis = 1)
    col_stand = X_undum.columns
    
    temp_use = df[col_stand]
    scaler = StandardScaler().fit(temp_use.values) ## Normalizer gave best score with default parameters
    temp_use = scaler.transform(temp_use.values)
    df_out[col_stand] = temp_use
    
    return df_out, scaler.mean_, scaler.var_

### get the difference of two lists
def diff(l1, l2):
    return list(set(l1) - set(l2)) + list(set(l2) - set(l1))

### Convert features to categorical features
def convert_categorical(data,features):
    
    for name in features:
        data[name] = data[name].astype('category')
    cat_columns = data.select_dtypes(['category']).columns
    data[cat_columns] = data[cat_columns].apply(lambda x: x.cat.codes)
    
    return data
    
### One-hot encoding of categorical features
def cat_encode(data, CATEGORICAL_FEATURES):
    
    for feature, values in CATEGORICAL_FEATURES.items():
        print(feature, values)
        unknown_cat = set(data[feature]).difference(values)
        assert not unknown_cat, 'categorical feature %s has unexpected value(s):\n%s'.format(feature, ', '.join(str(x) for x in unknown_cat))
        dtype = pd.api.types.CategoricalDtype(categories=values)
        data[feature] = data[feature].astype(dtype)

    return pd.get_dummies(data, columns=CATEGORICAL_FEATURES.keys(), prefix_sep='~')
    


if __name__ == "__main__":
    main(df, Numerical_col, Location_col, Data_col, Cat_col)

