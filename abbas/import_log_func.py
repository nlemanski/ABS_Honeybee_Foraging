# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 11:32:17 2018
Edited 8.28.18, 1.30.2021
Function to import the log files and summarize output over all repetitions

@author: natalie
"""

import numpy as np
import os

# function imports just one model treatment at a time (one patch #, scout #, and set of persistence values)
# calculates mean and sd for each variable and saves to a file
def import_log_summary(path,outpath,resource_type,num_patches,num_scouts,prst,num_repetitions,simulation_time):
    # Initialize array
    data = np.zeros((num_repetitions,simulation_time,5))
    # Import from file
    for rep in range(num_repetitions):
        fname = path+'Patches_'+str(num_patches)+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)+'/Log_'+resource_type+'_num_patches_'+str(num_patches)+'_scouts_'+str(num_scouts)+'_prst_'+str(prst)+'-'+str(rep)+'.log'
        data[rep,:,:] = np.genfromtxt(fname, delimiter = ' ')
    
    # average across all reps
    data_mean = np.mean(data,axis=0)
    data_std = np.std(data,axis=0)
    #disc = data_mean[:,0]# how many scouts found food at that time step
    #food = data_mean[:,1] #  food collected by all the scouts at time step
    #total_food = np.cumsum(food) # cumulative food collected so far
    #final_food = total_food[-1] # total food collected at end of simulation
    #energy_sct = data_mean[:,2] # total energy expenditure of scouts
    #energy_rct = data_mean[:,3]# total energy expenditure of recruits
    #prct_rct = data_mean[:,4] # percent of exploiters that are actively recruited
    
    meanname = outpath+'Patches_'+str(num_patches)+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)+'/Log_'+resource_type+'_num_patches_'+str(num_patches)+'_scouts_'+str(num_scouts)+'_prst_'+str(prst)+'-mean.txt'
    stdname = outpath+'Patches_'+str(num_patches)+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)+'/Log_'+resource_type+'_num_patches_'+str(num_patches)+'_scouts_'+str(num_scouts)+'_prst_'+str(prst)+'-std.txt'
    
    if not os.path.isdir(outpath+'Patches_'+str(num_patches)+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)):
        os.makedirs(outpath+'Patches_'+str(num_patches)+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst))
        
    np.savetxt(meanname,data_mean)
    np.savetxt(stdname,data_std)
    
    return #data_mean, data_std

# Inputs to the function 
path = 'abbas/model_output/resource_distribution/Logs/'
outpath = 'abbas/model_output/resource_distribution/Summaries/'
resource_type = 'Patchy'
simulation_time = 10000
num_repetitions = 100
patch_nums = range(9,11)
scout_nums = range(10,100,10)
perst_vals = ['3-3','3-5','5-3','5-5']

# Use function to import and summarize log files
for patch in range(len(patch_nums)):    
    num_patches = patch_nums[patch]
    print('importing patches '+str(num_patches))
    for ns in range(len(scout_nums)):
        num_scouts = scout_nums[ns]
        for pv in range(len(perst_vals)):
            prst = perst_vals[pv]
            import_log_summary(path,outpath,resource_type,num_patches,num_scouts,prst,num_repetitions,simulation_time)


def import_log_output(path,resource_type,num_scouts,num_repetitions,simulation_time):
    # Initialize arrays
    data = np.zeros((num_repetitions,simulation_time,5))
    disc = np.zeros((num_repetitions,simulation_time))
    food = np.zeros((num_repetitions,simulation_time))
    total_food = np.zeros((num_repetitions,simulation_time))
    final_food = np.zeros((num_repetitions))
    energy_sct = np.zeros((num_repetitions,simulation_time))
    energy_rct = np.zeros((num_repetitions,simulation_time))
    prct_rct = np.zeros((num_repetitions,simulation_time))
    # Put each output variable in its own array
    for rep in range(num_repetitions):
        fname = path+'/Log_'+resource_type+'_num_patches_'+str(num_patches)+'_scouts_'+str(num_scouts)+'-'+str(rep)+'.log'
        data[rep,:,:] = np.genfromtxt(fname, delimiter = ' ')
        disc[rep] = data[rep,:,0] # how many scouts found food at that time step
        food[rep] = data[rep,:,1] #  food collected by all the scouts at time step
        total_food[rep] = np.cumsum(food[rep]) # cumulative food collected so far
        final_food[rep] = total_food[rep,-1] # total food collected at end of simulation
        energy_sct[rep] = data[rep,:,2] # total energy expenditure of scouts
        energy_rct[rep] = data[rep,:,3] # total energy expenditure of recruits
        prct_rct[rep] = data[rep,:,4] # percent of exploiters that are actively recruited
    
    return disc, food, total_food, final_food, energy_sct, energy_rct, prct_rct

