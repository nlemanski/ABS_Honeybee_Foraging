# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 15:50:26 2018
Edited 1.30.2021

Examining how floral diversity and patchiness jointly affect optimal scout:recruit ratio and optimal persistence.

@author: natal
"""

import os
import sys
from math import *
import pylab as pl

# This assumes the folder 'abbas' is located in same folder as this script
sys.path.insert(0, './abbas/honeybee/')

from Forage_diversity import Forage
import numpy as np

# Simulation parameters
simulation_time = 21000 # changed from 10,000 to 21,000
num_repetitions = 1
lastrep = 0

# Number of bees`
total_bees  = 100 # total foragers in colony
scout_nums = range(10,100,10) # different percentages of scouts considered

# Persistence
perst_vals = [1,3,5,7,10,13,16,20] # different persistence values considered
#perst_vals = [16]

# Setting save locations
log_path = 'nlemanski/ABBAS/resource_distribution/model_output/Logs/'
plot_path = 'nlemanski/ABBAS/resource_distribution/model_output/Plots/resource_areas/diverse/'

# Describing the resource distribution
resource_type = 'Diverse'
edit = 'RPQ' # recruitment proportional to resource quality
total_food = int( (40**2)*0.6*3 ) # defines the average total amount of food
Nr = 1                            # number of patches of each type
num_patches = 3*Nr                # number of patches total
psize = int( sqrt(total_food/0.6/num_patches) )  # patch size depends on number of patches
R = 200                           # distance to patches from hive


# This defines a function that plots the resource distribution.
def plot_resources(area1, area2, area3, filename, color='Blues'):
    """ Assumes areas are the Forage Area variables, which
    contain the resources.
    """
    areas = area1 + 2*area2 + 3*area3
    pl.figure(figsize=(3,3))
    pl.matshow(areas, cmap = pl.get_cmap(color))
    pl.tight_layout()
    pl.savefig(filename, dpi=400, format='png')
    pl.close()

    return


for repetition in range(lastrep, num_repetitions):
    
    for num_scouts in scout_nums:
        num_recruits = total_bees - num_scouts
        
        for prst in perst_vals:
            scout_persistence = prst
            recruit_persistence = prst
            
            if not os.path.isdir(log_path+'/'+resource_type+edit +'/Scouts_'+ str(num_scouts) + '/prst_' + str(scout_persistence)+'-'+str(recruit_persistence)):
                os.makedirs(log_path+'/'+resource_type+edit +'/Scouts_'+ str(num_scouts) + '/prst_' + str(scout_persistence)+'-'+str(recruit_persistence))
            
            print('Running simulation - Repetition: %d' % repetition)
            # sim is an object we are creating in the class Forage (defined in Forage_diversity.py)
            sim = Forage(Nexplorer = num_scouts, Nexploiter = num_recruits,
                         T = simulation_time,
                         SctPersistence = scout_persistence,
                         RecPersistence = recruit_persistence)

            sim.resourcesDiverse(Nr=Nr, R=R, size=psize, ps=.6)
            
            # Plots the resources at the beginning of the simulation (only first rep)
            if repetition == 0:
                plotname = plot_path+'Plot_resources_initial_'+resource_type+edit+'_num_patches_'+str(num_patches)+'_scouts_'+str(num_scouts)+'_prst_'+str(scout_persistence)+'-'+str(recruit_persistence)+'_'+str(repetition)+'.png'
                plot_resources(sim.Area1,sim.Area2,sim.Area3,plotname)
            
            for time in range(simulation_time):
                sim.update()
                #print(sim.Area.sum())
                
            # Writing log files
            # One log file is saved for each run of simulation
            fname = log_path+'/'+resource_type+edit+'/Scouts_'+str(num_scouts)+'/prst_' + str(scout_persistence)+'-'+str(recruit_persistence)+'/Log_'+resource_type+'_scouts_'+str(num_scouts)+'_prst_'+str(scout_persistence)+'-'+str(recruit_persistence)+'-'+str(repetition)+'.log'
            #print('Printing: ' + fname)
            np.savetxt(fname, sim.Log)

            # Also plotting the resources at the end
            if repetition == 0:
                plotname = plot_path+'Plot_resources_final_'+resource_type+edit+'_num_patches_'+str(num_patches)+'_scouts_'+str(num_scouts)+'_prst_'+str(scout_persistence)+'-'+str(recruit_persistence)+'_'+str(repetition)+'.png'
                plot_resources(sim.Area1,sim.Area2,sim.Area3,plotname)


