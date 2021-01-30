# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 15:11:26 2018

violin plots of optimal scout numbers
@author: natal
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
#
try:
    len(data)
except:
    print('To use this script, you must first import log files')    
#
figpath = 'abbas/model_output/Plots/'
folder = 'violin/'

# violin plot
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4.5, 4))
axes.violinplot(final_food[0].tolist(),showmeans=False,showmedians=True)
plt.setp(axes, xticks=[y + 1 for y in range(len(final_food[0]))], xticklabels=scout_nums)
plt.show()
