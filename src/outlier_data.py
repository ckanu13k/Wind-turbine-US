#!/usr/bin/env python
# coding: utf-8

import numpy as np
### Include class here!!!
class outlier_prep:

    def __init__(self, data,  axe, col, lower=None, upper=None):
        self.data = data
        self.ax = axe
        self.lower = lower
        self.upper = upper
        self.col = col
 
    def outlier_aware_hist(self):
        if not self.lower or self.lower < self.data.min():
           self.lower = self.data.min()
           lower_outliers = False
        else:
           lower_outliers = True

        if not self.upper or self.upper > self.data.max():
           self.upper = self.data.max()
           upper_outliers = False
        else:
           upper_outliers = True

        n, bins, patches = self.ax.hist(self.data, range=(self.lower, self.upper), bins=12) #bins='auto')
        self.ax.set_title(self.col)
        if lower_outliers:
           n_lower_outliers = (self.data < self.lower).sum()
           patches[0].set_height(patches[0].get_height() + n_lower_outliers)
           patches[0].set_facecolor('c')
           patches[0].set_label('Lower outliers: ({:.2f}, {:.2f})'.format(self.data.min(), self.lower))

        if upper_outliers:
           n_upper_outliers = (self.data > self.upper).sum()
           patches[-1].set_height(patches[-1].get_height() + n_upper_outliers)
           patches[-1].set_facecolor('m')
           patches[-1].set_label('Upper outliers: ({:.2f}, {:.2f})'.format(self.upper, self.data.max()))

        if lower_outliers or upper_outliers:
           plt.legend()

    def mad(self):
        median = np.median(self.data)
        diff = np.abs(self.data - median)
        mad = np.median(diff)
        return mad

    def calculate_bounds(self, z_thresh=3.5):
        MAD = self.mad()
        median = np.median(self.data)
        const = z_thresh * MAD / 0.6745
        return (median - const, median + const)


    def outlier_data(self):
        if not self.lower or self.lower < self.data.min():
           self.lower = self.data.min()
           lower_outliers = False
        else:
           lower_outliers = True

        if not self.upper or self.upper > self.data.max():
           self.upper = self.data.max()
           upper_outliers = False
        else:
           upper_outliers = True

        self.data[self.data < self.lower] = np.nan
        self.data[self.data > self.upper] = np.nan
        return self.data
