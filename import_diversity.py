# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 15:46:51 2018, edited 1.30.2021

Create and use functions to import and summarize log files for ABBAS model with different quality resources. Imports dispersed and 
clumped resource distributions.

@author: Natalie
"""
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
import pylab as pl

### Create Functions For Importing Logs ###

# import a single log file
def import_diversity(path,resource_type,extra,num_scouts,prst,num_repetitions,simulation_time):
    
    import numpy as np
    data = np.zeros((num_repetitions,simulation_time,8))
    for rep in range(num_repetitions):
        fname = path+resource_type+extra+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)+'/Log_'+resource_type+'_scouts_'+str(num_scouts)+'_prst_'+str(prst)+'-'+str(rep)+'.log'
        data[rep,:,:] = np.genfromtxt(fname)#, delimiter = ' ')
        
    return data

# Summarize across reps and save mean and SD to file
def sum_diversity(outpath,data,resource_type,num_scouts,prst):
    
    import numpy as np
    import os
    
    data_mean = np.mean(data,axis=0)
    data_std = np.std(data,axis=0)
    
    if not os.path.isdir(outpath+resource_type+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)):
        os.makedirs(outpath+resource_type+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst))
        
    meanname = outpath+resource_type+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)+'/Log_'+resource_type+'_scouts_'+str(num_scouts)+'_prst_'+str(prst)+'-mean.txt'
    stdname =  outpath+resource_type+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)+'/Log_'+resource_type+'_scouts_'+str(num_scouts)+'_prst_'+str(prst)+'-std.txt'
    
    if not os.path.isdir(outpath+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)):
        os.makedirs(     outpath+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst))
        
    np.savetxt(meanname,data_mean)
    np.savetxt(stdname,data_std)
    
    return #data_mean, data_std

# Cumulative food collected over time
def cum_food(data):
    import numpy as np
    food = data[:,1]
    csfood = np.cumsum(food, axis=0)
    
    return csfood

# Total amount of food collected at end of simulation
def final_food(data):
    
    import numpy as np
    food = data[:,1]
    end_food = np.sum(food, axis=0)
    
    return end_food

def net_food(data):
    
    import numpy as np
    food = data[:,1]
    total_food = np.cumsum(food)
    end_food = total_food[-1]
    sct_energy = data[:,2]
    rct_energy = data[:,3]
    
    net_food = end_food - rct_energy[-1] - sct_energy[-1]
    
    return net_food
    
### Use functions to import and summarize log files ###

# filepath where logs stored
path = 'ABBAS/model_output/diversity/Logs/'
# filepath for results averaged across all reps to be stored
outpath = 'ABBAS/model_output/diversity/Summaries/'
#filepath for processed results to be stored
sumpath = 'ABBAS/model_output/Results/'

# simulation parameters
simulation_time = 21000
num_repetitions = 150
scout_nums = range(10,100,10)
perst_vals = [1,3,5,7,10,13,16,20]
# perst_vals = [10,20] # used in published model

# set up empty arrays and define type of resource distribution being modeled
resource_type = 'Diverse' # dispersed resource patches with variable quality
extra = "RPQ"  # probability of recruitment proportional to resource quality
tfood_dispersed = np.zeros((num_repetitions,len(scout_nums),len(perst_vals))) # total food collected, all reps
tfood_dis_m = np.zeros((len(scout_nums),len(perst_vals)))
tfood_dis_sd = np.zeros((len(scout_nums),len(perst_vals)))
nfood_dispersed = np.zeros((num_repetitions,len(scout_nums),len(perst_vals))) # net food collected, minus energy expended searching, all reps
nfood_dis_m = np.zeros((len(scout_nums),len(perst_vals)))
nfood_dis_sd = np.zeros((len(scout_nums),len(perst_vals)))
optscout_t_dispersed = np.zeros((len(perst_vals))) # optimal scout percentage for a given level of persistence
optscout_n_dispersed = np.zeros((len(perst_vals))) # optimal scout percentage for a given level of persistence
cumfood_dispersed = np.zeros((num_repetitions,len(scout_nums),len(perst_vals),simulation_time))
cumfood_dis_m = np.zeros((len(scout_nums),len(perst_vals),simulation_time))
cumfood_dis_sd = np.zeros((len(scout_nums),len(perst_vals),simulation_time))
lowvisits_dis = np.zeros((num_repetitions,len(scout_nums),len(perst_vals)))
medvisits_dis = np.zeros((num_repetitions,len(scout_nums),len(perst_vals)))
highvisits_dis = np.zeros((num_repetitions,len(scout_nums),len(perst_vals)))

# import all log files for all scout nums and persistence values for dispersed distribution
for perst in perst_vals:
    j = perst_vals.index(perst)
    prst = str(perst)+'-'+str(perst)
    print('Importing persistence '+str(perst))
    for num_scouts in scout_nums:
        i = scout_nums.index(num_scouts)
        print('Importing scouts '+str(num_scouts))
        data = import_diversity(path,resource_type,extra,num_scouts,prst,num_repetitions,simulation_time) #import all variables for all reps
        sum_diversity(outpath,data,resource_type+extra,num_scouts,prst)
        for k in range(num_repetitions):
            tfood_dispersed[k,i,j] = final_food(data[k,:,:]) # total food collected in rep k, scout number i, persistence j
            nfood_dispersed[k,i,j] = net_food(data[k,:,:])   # net food collected in rep k, scout number i, persistence j
            cumfood_dispersed[k,i,j,:] = cum_food(data[k,:,:])
            lowvisits_dis[k,i,j] = np.sum(data[k,:,5]) # total visits to low quality patch by end of sim
            medvisits_dis[k,i,j] = np.sum(data[k,:,6]) # total visits to medium quality patch by end of sim
            highvisits_dis[k,i,j] = np.sum(data[k,:,7]) # total visits to high quality patch by end of sim
        
        tfood_dis_m[i,j] = np.mean(tfood_dispersed[:,i,j],axis=0) # mean total food collected across all reps, scout num i, perst j
        tfood_dis_sd[i,j] = np.std(tfood_dispersed[:,i,j],axis=0) # standard deviation of total food collected across all reps, scout num i, perst j
        nfood_dis_m[i,j] = np.mean(nfood_dispersed[:,i,j],axis=0) # mean net food collected across all reps, scout num i, perst j
        nfood_dis_sd[i,j] = np.std(nfood_dispersed[:,i,j],axis=0) # standard deviation of net food across all reps
        cumfood_dis_m[i,j,:] = np.mean(cumfood_dispersed[:,i,j,:],axis=0) # mean cumulative food collected over time
        cumfood_dis_sd[i,j,:] = np.std(cumfood_dispersed[:,i,j,:],axis=0) # sd of cumulative food collected over time
        
    optscout_t_dispersed[j] = scout_nums[np.argmax(tfood_dis_m[:,j])] #optimal % of scouts, based on total food
    optscout_n_dispersed[j] = scout_nums[np.argmax(nfood_dis_m[:,j])] #optimal % of scouts, based on net food

print('Import complete- dispersed')

# set up empty arrays and name resource type
resource_type = 'DiverseClumped' # variable quality resource patches, clumped distribution
extra = "RPQ"  # recruitment proportional to resource quality
tfood_clumped = np.zeros((num_repetitions,len(scout_nums),len(perst_vals))) # total food collected, all reps
tfood_clu_m = np.zeros((len(scout_nums),len(perst_vals)))
tfood_clu_sd = np.zeros((len(scout_nums),len(perst_vals)))
nfood_clumped = np.zeros((num_repetitions,len(scout_nums),len(perst_vals))) # net food collected, minus energy expended searching, all reps
nfood_clu_m = np.zeros((len(scout_nums),len(perst_vals)))
nfood_clu_sd = np.zeros((len(scout_nums),len(perst_vals)))
optscout_t_clumped = np.zeros((len(perst_vals))) # optimal scout percentage for a given level of persistence
optscout_n_clumped = np.zeros((len(perst_vals))) # optimal scout percentage for a given level of persistence
cumfood_clumped = np.zeros((num_repetitions,len(scout_nums),len(perst_vals),simulation_time))
cumfood_clu_m = np.zeros((len(scout_nums),len(perst_vals),simulation_time))
cumfood_clu_sd = np.zeros((len(scout_nums),len(perst_vals),simulation_time))
lowvisits_clu = np.zeros((num_repetitions,len(scout_nums),len(perst_vals)))
medvisits_clu = np.zeros((num_repetitions,len(scout_nums),len(perst_vals)))
highvisits_clu = np.zeros((num_repetitions,len(scout_nums),len(perst_vals)))

# import all log files for all scout nums and persistence values for clumped distribution
for perst in perst_vals:
    j = perst_vals.index(perst)
    prst = str(perst)+'-'+str(perst)
    print('Importing persistence '+str(perst))
    for num_scouts in scout_nums:
        i = scout_nums.index(num_scouts)
        print('Importing scouts'+str(num_scouts))
        data = import_diversity(path,resource_type,extra,num_scouts,prst,num_repetitions,simulation_time) #import all reps
        sum_diversity(outpath,data,resource_type+extra,num_scouts,prst)
        for k in range(num_repetitions):
            tfood_clumped[k,i,j] = final_food(data[k,:,:]) # total food collected in rep k, scout number i, persistence j
            nfood_clumped[k,i,j] = net_food(data[k,:,:])   # net food collected in rep k, scout number i, persistence j
            cumfood_clumped[k,i,j,:] = cum_food(data[k,:,:])
            lowvisits_clu[k,i,j] = np.sum(data[k,:,5]) # total visits to low quality patch by end of sim
            medvisits_clu[k,i,j] = np.sum(data[k,:,6]) # total visits to medium quality patch by end of sim
            highvisits_clu[k,i,j] = np.sum(data[k,:,7]) # total visits to high quality patch by end of sim
        
        tfood_clu_m[i,j] = np.mean(tfood_clumped[:,i,j],axis=0) # mean total food collected across all reps, scout num i, perst j
        tfood_clu_sd[i,j] = np.std(tfood_clumped[:,i,j],axis=0) # standard deviation of total food collected across all reps, scout num i, perst j
        nfood_clu_m[i,j] = np.mean(nfood_clumped[:,i,j],axis=0) # mean net food collected across all reps, scout num i, perst j
        nfood_clu_sd[i,j] = np.std(nfood_clumped[:,i,j],axis=0) # standard deviation of net food across all reps
        cumfood_clu_m[i,j,:] = np.mean(cumfood_clumped[:,i,j,:],axis=0) # mean cumulative food collected over time
        cumfood_clu_sd[i,j,:] = np.std(cumfood_clumped[:,i,j,:],axis=0) # sd of cumulative food collected over time
        
    optscout_t_clumped[j] = scout_nums[np.argmax(tfood_clu_m[:,j])] #optimal % of scouts, based on total food
    optscout_n_clumped[j] = scout_nums[np.argmax(nfood_clu_m[:,j])] #optimal % of scouts, based on net food

print('Import complete- clumped')

## find mean and SD of visits to low, med, and high quality food patches
# clumped visits
vis_low_clu_m   = np.mean(lowvisits_clu, axis=0)
vis_low_clu_sd  = np.std(lowvisits_clu, axis=0)
vis_med_clu_m   = np.mean(medvisits_clu, axis=0)
vis_med_clu_sd  = np.std(medvisits_clu, axis=0)
vis_high_clu_m  = np.mean(highvisits_clu, axis=0)
vis_high_clu_sd = np.std(highvisits_clu, axis=0)

# dispersed visits
vis_low_dis_m   = np.mean(lowvisits_dis, axis=0)
vis_low_dis_sd  = np.std(lowvisits_dis, axis=0)
vis_med_dis_m   = np.mean(medvisits_dis, axis=0)
vis_med_dis_sd  = np.std(medvisits_dis, axis=0)
vis_high_dis_m  = np.mean(highvisits_dis, axis=0)
vis_high_dis_sd = np.std(highvisits_dis, axis=0)

## save mean of processed results to files
fname = sumpath+'total_food_clumped_mean.csv' # save mean total food collected to file
np.savetxt(fname,tfood_clu_m,delimiter=',')
fname = sumpath+'total_food_dispersed_mean.csv'
np.savetxt(fname,tfood_dis_m,delimiter=',')

fname = sumpath+'net_food_clumped_mean.csv' # save mean net food collected to file
np.savetxt(fname,nfood_clu_m,delimiter=',')
fname = sumpath+'net_food_dispersed_mean.csv'
np.savetxt(fname,nfood_dis_m,delimiter=',')

fname = sumpath+'visits_low_clumped_mean.csv' # save mean visits to low quality feeder to file
np.savetxt(fname,vis_low_clu_m,delimiter=',')
fname = sumpath+'visits_low_dispersed_mean.csv'
np.savetxt(fname,vis_low_dis_m,delimiter=',')

fname = sumpath+'visits_med_clumped_mean.csv' # save mean visits to med quality feeder to file
np.savetxt(fname,vis_med_clu_m,delimiter=',')
fname = sumpath+'visits_med_dispersed_mean.csv'
np.savetxt(fname,vis_med_dis_m,delimiter=',')

fname = sumpath+'visits_high_clumped_mean.csv' # save mean visits to high quality feeder to file
np.savetxt(fname,vis_high_clu_m,delimiter=',')
fname = sumpath+'visits_high_dispersed_mean.csv'
np.savetxt(fname,vis_high_dis_m,delimiter=',')

## save standard deviations of processed results to files
fname = sumpath+'total_food_clumped_sd.csv' # save sd total food collected to file
np.savetxt(fname,tfood_clu_sd,delimiter=',')
fname = sumpath+'total_food_dispersed_sd.csv'
np.savetxt(fname,tfood_dis_sd,delimiter=',')

fname = sumpath+'net_food_clumped_sd.csv' # save sd net food collected to file
np.savetxt(fname,nfood_clu_sd,delimiter=',')
fname = sumpath+'net_food_dispersed_sd.csv'
np.savetxt(fname,nfood_dis_sd,delimiter=',')

fname = sumpath+'visits_low_clumped_sd.csv' # save sd visits to low quality feeder to file
np.savetxt(fname,vis_low_clu_sd,delimiter=',')
fname = sumpath+'visits_low_dispersed_sd.csv'
np.savetxt(fname,vis_low_dis_sd,delimiter=',')

fname = sumpath+'visits_med_clumped_sd.csv' # save sd visits to med quality feeder to file
np.savetxt(fname,vis_med_clu_sd,delimiter=',')
fname = sumpath+'visits_med_dispersed_sd.csv'
np.savetxt(fname,vis_med_dis_sd,delimiter=',')

fname = sumpath+'visits_high_clumped_sd.csv' # save sd visits to high quality feeder to file
np.savetxt(fname,vis_high_clu_sd,delimiter=',')
fname = sumpath+'visits_high_dispersed_sd.csv'
np.savetxt(fname,vis_high_dis_sd,delimiter=',')
