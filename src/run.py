#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import time

import data_prep
from kmeans_ml import run_kmean
import model_eval
np.random.seed(0)


### Start with the data
df = pd.read_csv("wind_turbines.csv")

### Split the feature as its kind
Numerical_col = ['Turbine.Capacity','Turbine.Hub_Height', 'Turbine.Rotor_Diameter', 'Turbine.Swept_Area','Turbine.Total_Height', 'Project.Capacity', 'Project.Number_Turbines']
Location_col = ['Site.Latitude', 'Site.Longitude']
Data_col = ['Year']
Cat_col = ['Site.State', 'Site.County']

### Prep the data
pca_Df, pca = data_prep.main(df, Numerical_col, Location_col, Data_col, Cat_col)

### Run ml on data
batch_size=15
n_clusters=3
scr_kmean, scr_mini_kmean, k_means_class, k_mbk_class = run_kmean(pca_Df, batch_size, n_clusters)

### Evaluate model
model_eval.model_eval(df, pca_Df, pca, k_means_class, k_mbk_class, 'Site.Latitude', 'Site.Longitude', 'Year', Numerical_col)

