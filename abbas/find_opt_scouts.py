# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 15:01:01 2018, edited 9/8/18, 1.30.21
Analyze abbas model output
Find optimal scouting ratio for different patchiness and persistence values, plot and save to files
@author: natalie
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl

# filepaths
path = 'abbas/model_output/resource_distribution/Summaries/'
figpath = 'abbas/model_output/Plots/optimal_scout_ratio/'

# parameters
resource_type = 'Patchy'
simulation_time = 10000
patch_nums = range(3,11)
scout_nums = range(10,100,10)
perst_vals = ['3-3','3-5','5-3','5-5']

### create function to find optimal number of scouts  ###
def opt_scouts(path,resource_type,scout_nums,num_patches,prst,simulation_time):
    final_food = []
    for num_scouts in scout_nums:
        fname = path+'Patches_'+str(num_patches)+'/Scouts_'+str(num_scouts)+'/prst_'+str(prst)+'/Log_'+resource_type+'_num_patches_'+str(num_patches)+'_scouts_'+str(num_scouts)+'_prst_'+str(prst)+'-mean.txt'
        data = np.zeros((simulation_time,5))
        data[:,:] = np.genfromtxt(fname, delimiter = ' ')
        food = data[:,1]
        total_food = np.cumsum(food)
        end_food = total_food[-1]
        final_food.append(end_food)
    
    opt_scout = scout_nums[np.argmax(final_food)]
    
    return opt_scout, final_food

# use function to find optimal scouts for each persistence value and patch number
optimal_scouts = np.zeros((len(patch_nums),len(perst_vals)))
final_foods = np.zeros((len(perst_vals),len(patch_nums),len(scout_nums)))
for n in range(len(patch_nums)):
    num_patches = patch_nums[n]
    print(num_patches)
    for p in range(len(perst_vals)):
        prst = perst_vals[p]
        optimal_scouts[n,p],final_foods[p,n,:] = opt_scouts(path,resource_type,scout_nums,num_patches,prst,simulation_time)

# save optimal scouts to a file
fname = path+'optimal_scouts_prst_patchnum.txt'
np.savetxt(fname,optimal_scouts)

# line plot optimal scout number as function of both persistence and patch number
plt.plot(patch_nums,optimal_scouts[:,0], marker='^',color='blue')
plt.plot(patch_nums,optimal_scouts[:,1], marker='^',color='red' ,linestyle=':')
plt.plot(patch_nums,optimal_scouts[:,2], marker='o',color='blue')
plt.plot(patch_nums,optimal_scouts[:,3], marker='o',color='red' ,linestyle=':')
plt.ylabel('Optimal Scout Percentage')
plt.xlabel('Number of Food Patches')
pkey = ['Low, low','Low, high','High, low','High, high']
plt.legend(pkey)
plt.title('Effect of persistence and resource patchiness on optimal scout ratio')
figname = 'perst_patch_opt_scout_num.png'
plt.savefig(figpath+figname, dpi=400, format='png')

# plot food collected vs patch number and scout number
fig = plt.figure()
st = fig.suptitle("Effect of scout number and patchiness on food collected", fontsize="x-large")

ax1 = fig.add_subplot(221)
ax1.pcolormesh(final_foods[0,:,:])
plt.xticks([])
plt.yticks(np.arange(len(patch_nums)),patch_nums)
ax1.set_title("lolo")

ax2 = fig.add_subplot(222)
ax2.pcolormesh(final_foods[1,:,:])
plt.xticks([])
plt.yticks(np.arange(len(patch_nums)),patch_nums)
ax2.set_title("lohi")

ax3 = fig.add_subplot(223)
ax3.pcolormesh(final_foods[2,:,:])
plt.xticks(np.arange(len(scout_nums)),scout_nums)
plt.yticks(np.arange(len(patch_nums)),patch_nums)
ax3.set_title("hilo")

ax4 = fig.add_subplot(224)
ax4.pcolormesh(final_foods[3,:,:])
plt.xticks(np.arange(len(scout_nums)),scout_nums)
plt.yticks(np.arange(len(patch_nums)),patch_nums)
ax4.set_title("hihi")

fig.text(0.5, 0.02, 'Percent Scouts', ha='center')
fig.text(0.04, 0.5, 'Number of Food Patches', va='center', rotation='vertical')

figname = 'food_collected.png'
plt.savefig(figpath+figname, dpi=400, format='png')


