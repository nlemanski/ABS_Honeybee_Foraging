# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 21:44:33 2018, edited 11.21.2018, 5.17.29, 1.30.2021

Plot simulation results for diverse clumped and diverse dispersed resource distributions.
Calculate some summary statistics about the simulated results and export.

@author: natal
"""
# import packages
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pylab as pl
import math

### This assumes code import_diversity.py has run to import files ###

# filepath where plots stored
figpath = 'ABBAS/model_output/Plots/'

# Parameters
nr = num_repetitions

### Summarize visit data ###
highvisits_clu_m = np.mean(highvisits_clu,axis=0)
medvisits_clu_m = np.mean(medvisits_clu,axis=0)
lowvisits_clu_m = np.mean(lowvisits_clu,axis=0)
highvisits_dis_m = np.mean(highvisits_dis,axis=0)
medvisits_dis_m = np.mean(medvisits_dis,axis=0)
lowvisits_dis_m = np.mean(lowvisits_dis,axis=0)

highvisits_clu_sd = np.std(highvisits_clu,axis=0)
medvisits_clu_sd = np.std(medvisits_clu,axis=0)
lowvisits_clu_sd = np.std(lowvisits_clu,axis=0)
highvisits_dis_sd = np.std(highvisits_dis,axis=0)
medvisits_dis_sd = np.std(medvisits_dis,axis=0)
lowvisits_dis_sd = np.std(lowvisits_dis,axis=0)

### create variable for total number of visits to all feeders ###
totalvisits_clu = highvisits_clu + medvisits_clu + lowvisits_clu
totalvisits_dis = highvisits_dis + medvisits_dis + lowvisits_dis

totalvisits_clu_m  = np.mean(totalvisits_clu,axis=0)
totalvisits_clu_sd = np.std(totalvisits_clu,axis=0)
totalvisits_dis_m  = np.mean(totalvisits_dis,axis=0)
totalvisits_dis_sd = np.std(totalvisits_dis,axis=0)


### make pretty plots ###

# plot optimal scout number vs persistence, based on total food
plt.plot(perst_vals, optscout_t_dispersed, 'b-o', perst_vals, optscout_t_clumped, 'r:^')
plt.ylabel('Optimal % Scouts')
plt.xlabel('Persistence')
plt.legend(['Resources Dispersed','Resources Clumped'])
plt.show()
figname = 'optimal_scouts_diversity_rpq.png'
plt.savefig(figpath+figname, dpi=400, format='png')

# plot optimal scout number vs persistence, based on net food
plt.plot(perst_vals, optscout_n_dispersed, 'b-o', perst_vals, optscout_n_clumped, 'r:^')
plt.ylabel('Optimal % Scouts')
plt.xlabel('Persistence')
plt.legend(['Resources Dispersed','Resources Clumped'])
plt.show()
figname = 'optimal_scouts_net_diversity_rpq.png'
plt.savefig(figpath+figname, dpi=400, format='png')

#plot total food collected as function of scout # for different persistence levels
# show mean and standard deviation across reps
plot1 = plt.subplot(1,2,1)
for j in range(len(perst_vals)):
    plt.errorbar(scout_nums, tfood_dis_m[:,j], yerr=tfood_dis_sd[:,j])
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.ylabel('Total Food Collected')
plt.title('Resources Dispersed')

plt.subplot(1,2,2)
for j in range(len(perst_vals)):
    plt.errorbar(scout_nums, tfood_clu_m[:,j], yerr=tfood_clu_sd[:,j])
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.title('Resources Clumped')
plt.legend(perst_vals)
plt.show()
figname = 'total_food_diversity_rpq_ebar.png'
plt.savefig(figpath+figname, dpi=400, format='png')

# plot total food collected as function of scout number for different persistence levels
# show mean and standard error across reps
nr = num_repetitions
plot1 = plt.subplot(1,2,1)
for j in range(len(perst_vals)):
    plt.errorbar(scout_nums, tfood_dis_m[:,j], yerr=(tfood_dis_sd[:,j]/math.sqrt(nr)))
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.ylabel('Total Food Collected')
plt.title('Resources Dispersed')

plt.subplot(1,2,2)
for j in range(len(perst_vals)):
    plt.errorbar(scout_nums, tfood_clu_m[:,j], yerr=(tfood_clu_sd[:,j]/math.sqrt(nr)))
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.title('Resources Clumped')
plt.legend(perst_vals)
plt.show()
figname = 'total_food_diversity_rpq_se.png'
plt.savefig(figpath+figname, dpi=400, format='png')

# plot net food collected as function of scout number for different persistence levels
# plot mean and sd across reps
plot2 = plt.subplot(1,2,1)
for j in range(len(perst_vals)):
    plt.errorbar(scout_nums, nfood_dis_m[:,j], yerr=nfood_dis_sd[:,j])
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.ylabel('Net Food Collected')
plt.title('Resources Dispersed')

plt.subplot(1,2,2)
for j in range(len(perst_vals)):
    plt.errorbar(scout_nums, nfood_clu_m[:,j], yerr=nfood_clu_sd[:,j])
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.title('Resources Clumped')
plt.legend(perst_vals)
plt.show()
figname = 'net_food_diversity_rpq_ebar.png'
plt.savefig(figpath+figname, dpi=400, format='png')

# plot net food collected as function of scout # for different persistence levels
# plot mean and se across reps
nr = num_repetitions
plot2 = plt.subplot(1,2,1)
for j in range(len(perst_vals)):
    plt.errorbar(scout_nums, nfood_dis_m[:,j], yerr=(nfood_dis_sd[:,j]/math.sqrt(nr)))
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.ylabel('Net Food Collected')
plt.title('Resources Dispersed')

plt.subplot(1,2,2)
for j in range(len(perst_vals)):
    plt.errorbar(scout_nums, nfood_clu_m[:,j], yerr=(nfood_clu_sd[:,j]/math.sqrt(nr)))
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.title('Resources Clumped')
plt.legend(perst_vals)
plt.show()
figname = 'net_food_diversity_rpq_se.png'
plt.savefig(figpath+figname, dpi=400, format='png')

# heatmap of total food collected, with scout number and persistence
fig = plt.figure()
st = fig.suptitle('Effect of scout number and persistence on total food collected',fontsize="x-large")

ax1 = fig.add_subplot(121)
mesh1 = ax1.imshow(tfood_dis_m, vmin=np.min(tfood_clu_m), vmax=np.max(tfood_clu_m))
plt.title('Resources Dispersed')
plt.xticks(np.arange(len(perst_vals)),perst_vals)
plt.yticks(np.arange(len(scout_nums)),scout_nums)
plt.ylabel('Percent Scouts')
plt.xlabel('Persistence')
#plt.colorbar(mappable=mesh1, ax=ax1)

ax2 = fig.add_subplot(122)
mesh2 = ax2.imshow(tfood_clu_m, vmin=np.min(tfood_clu_m), vmax=np.max(tfood_clu_m))
plt.title('Resources Clumped')
plt.xticks(np.arange(len(perst_vals)),perst_vals)
plt.yticks(np.arange(len(scout_nums)),scout_nums)
plt.xlabel('Persistence')
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
plt.colorbar(mappable=mesh2, cax=cbar_ax)
plt.show()
figname = 'heat_scoutnum_persistence_rpq.png'
plt.savefig(figpath+figname, dpi=400, format='png')

### plot net food collected as function  of scout number with subset of persistence values ###
# plot mean and standard errors
nr=num_repetitions 
plot3 = plt.subplot(1,2,1)
for j in [0,4,7]:
    plt.errorbar(scout_nums, nfood_dis_m[:,j], yerr=(nfood_dis_sd[:,j]/math.sqrt(nr)))
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.ylabel('Net Food Collected')
plt.title('Resources Dispersed')

plt.subplot(1,2,2)
for j in [0,4,7]:
    plt.errorbar(scout_nums, nfood_clu_m[:,j], yerr=(nfood_clu_sd[:,j]/math.sqrt(nr)))
plt.ylim([0,5000])
plt.xlabel('% Scouts')
plt.title('Resources Clumped')
plt.legend([1,10,20])
plt.show()
figname = 'net_food_diversity_rpq_subset.png'
plt.savefig(figpath+figname, dpi=400, format='png')

# make a single plot of food collected vs scout num with both clumped and dispersed on the same axis
# persistence = 20
plot4 = plt.figure()
ax4 = plot4.add_subplot(111)
#ax4.errorbar(scout_nums, nfood_dis_m[:,0], yerr=(nfood_dis_sd[:,0]/math.sqrt(nr)),color='cornflowerblue', 
#             linestyle='--', label='Dispersed-Perst 1')
#ax4.errorbar(scout_nums, nfood_dis_m[:,4], yerr=(nfood_dis_sd[:,4]/math.sqrt(nr)),color='blue', 
#             linestyle='--', label='Dispersed-Perst 10')
ax4.errorbar(scout_nums, nfood_dis_m[:,1], yerr=(nfood_dis_sd[:,1]/math.sqrt(nr)),color='blue', 
             linestyle='--', label='Resources Dispersed')
#ax4.errorbar(scout_nums, nfood_clu_m[:,0], yerr=(nfood_clu_sd[:,0]/math.sqrt(nr)),color='salmon', 
#             label='Clumped-Perst 1')
#ax4.errorbar(scout_nums, nfood_clu_m[:,4], yerr=(nfood_clu_sd[:,4]/math.sqrt(nr)),color='red', 
#             label='Clumped-Perst 10')
ax4.errorbar(scout_nums, nfood_clu_m[:,1], yerr=(nfood_clu_sd[:,1]/math.sqrt(nr)),color='red', 
             label='Resources Clumped')

plt.xlabel('% Scouts')
plt.ylabel('Net Food Collected (microL)')
plt.legend()
figname = 'net_food_optimalscouts_prst20.png'
plt.savefig(figpath+figname, dpi=400, format='png')

### Make sample plots of food collected over time for a few different treatments ###
# One minute is 50 time steps. One hour = 3000 time steps
hours = []
for t in range(simulation_time):
    hours.append(t/3000.)
    
# Food dispersed #
    
# Food dispersed, 10% scouts
# Divided food collected by 1000 to convert from microliters to mL
foods_low = cumfood_dis_m[scout_nums.index(10),perst_vals.index(1),:]/1000
errors_low = cumfood_dis_sd[scout_nums.index(10),perst_vals.index(1),:]/1000
foods_med = cumfood_dis_m[scout_nums.index(10),perst_vals.index(10),:]/1000
errors_med = cumfood_dis_sd[scout_nums.index(10),perst_vals.index(10),:]/1000
foods_high = cumfood_dis_m[scout_nums.index(10),perst_vals.index(20),:]/1000
errors_high = cumfood_dis_sd[scout_nums.index(10),perst_vals.index(20),:]/1000 

plot4 = plt.subplot(3,1,1)
plt.suptitle('Dispersed Distribution')
plt.errorbar(hours,foods_low,yerr=errors_low,ecolor='0.9',color='salmon')
plt.errorbar(hours,foods_med,yerr=errors_med,ecolor='0.9',color='red',linestyle='--')
plt.errorbar(hours,foods_high,yerr=errors_high,ecolor='0.9',color='darkred',linestyle=':')
plt.ylim([0,5])
plt.xticks([])
plt.legend(['Persistence = 1','Persistence = 10','Persistence = 20'])
plt.title('10% Scouts')

# Food dispersed, 50% scouts
plt.subplot(3,1,2)
# Divided food collected by 1000 to convert from microliters to mL
foods_low = cumfood_dis_m[scout_nums.index(50),perst_vals.index(1),:]/1000
errors_low = cumfood_dis_sd[scout_nums.index(50),perst_vals.index(1),:]/1000
foods_med = cumfood_dis_m[scout_nums.index(50),perst_vals.index(10),:]/1000
errors_med = cumfood_dis_sd[scout_nums.index(50),perst_vals.index(10),:]/1000
foods_high = cumfood_dis_m[scout_nums.index(50),perst_vals.index(20),:]/1000
errors_high = cumfood_dis_sd[scout_nums.index(50),perst_vals.index(20),:]/1000 

plt.errorbar(hours,foods_low,yerr=errors_low,ecolor='0.9',color='salmon')
plt.errorbar(hours,foods_med,yerr=errors_med,ecolor='0.9',color='red',linestyle='--')
plt.errorbar(hours,foods_high,yerr=errors_high,ecolor='0.9',color='darkred',linestyle=':')
plt.ylim([0,5])
plt.xticks([])
plt.ylabel('Food collected (mL)')
plt.title('50% Scouts')

# Food dispersed, 90% scouts
plt.subplot(3,1,3)
# Divided food collected by 1000 to convert from microliters to mL
foods_low = cumfood_dis_m[scout_nums.index(90),perst_vals.index(1),:]/1000
errors_low = cumfood_dis_sd[scout_nums.index(90),perst_vals.index(1),:]/1000
foods_med = cumfood_dis_m[scout_nums.index(90),perst_vals.index(10),:]/1000
errors_med = cumfood_dis_sd[scout_nums.index(90),perst_vals.index(10),:]/1000
foods_high = cumfood_dis_m[scout_nums.index(90),perst_vals.index(20),:]/1000
errors_high = cumfood_dis_sd[scout_nums.index(90),perst_vals.index(20),:]/1000 

plt.errorbar(hours,foods_low,yerr=errors_low,ecolor='0.9',color='salmon')
plt.errorbar(hours,foods_med,yerr=errors_med,ecolor='0.9',color='red',linestyle='--')
plt.errorbar(hours,foods_high,yerr=errors_high,ecolor='0.9',color='darkred',linestyle=':')
plt.ylim([0,5])
#plt.yticks([])
plt.xlabel('Time (hours)')
plt.title('90% Scouts')

figname = 'food_collected_by_time_dispersed_vert.png'
plt.savefig(figpath+figname, dpi=500, format='png')

# Food Clumped #

# 10% scouts
plot5 = plt.subplot(3,1,1)
plt.suptitle('Clumped Distribution')
# Divided food collected by 1000 to convert from microliters to mL
foods_low = cumfood_clu_m[scout_nums.index(10),perst_vals.index(1),:]/1000 # low persistence (1)
errors_low = cumfood_clu_sd[scout_nums.index(10),perst_vals.index(1),:]/1000
foods_med = cumfood_clu_m[scout_nums.index(10),perst_vals.index(10),:]/1000 # med persistence (10)
errors_med = cumfood_clu_sd[scout_nums.index(10),perst_vals.index(10),:]/1000
foods_high = cumfood_clu_m[scout_nums.index(10),perst_vals.index(20),:]/1000 # high persistence (20)
errors_high = cumfood_clu_sd[scout_nums.index(10),perst_vals.index(20),:]/1000 

plt.errorbar(hours,foods_low,yerr=errors_low,ecolor='0.9',color='cornflowerblue')
plt.errorbar(hours,foods_med,yerr=errors_med,ecolor='0.9',color='blue',linestyle='--')
plt.errorbar(hours,foods_high,yerr=errors_high,ecolor='0.9',color='navy',linestyle=':')
plt.ylim([0,5])
plt.xticks([])
plt.title('10% Scouts')
plt.legend(['Persistence = 1','Persistence = 10','Persistence = 20'],loc=2)

# 50% scouts
plt.subplot(3,1,2)
# Divided food collected by 1000 to convert from microliters to mL
foods_low = cumfood_clu_m[scout_nums.index(50),perst_vals.index(1),:]/1000
errors_low = cumfood_clu_sd[scout_nums.index(50),perst_vals.index(1),:]/1000
foods_med = cumfood_clu_m[scout_nums.index(50),perst_vals.index(10),:]/1000
errors_med = cumfood_clu_sd[scout_nums.index(50),perst_vals.index(10),:]/1000
foods_high = cumfood_clu_m[scout_nums.index(50),perst_vals.index(20),:]/1000
errors_high = cumfood_clu_sd[scout_nums.index(50),perst_vals.index(20),:]/1000 

plt.errorbar(hours,foods_low,yerr=errors_low,ecolor='0.9',color='cornflowerblue')
plt.errorbar(hours,foods_med,yerr=errors_med,ecolor='0.9',color='blue',linestyle='--')
plt.errorbar(hours,foods_high,yerr=errors_high,ecolor='0.9',color='navy',linestyle=':')
plt.ylim([0,5])
plt.ylabel('Food collected (mL)')
plt.xticks([])
plt.title('\n50% Scouts')

# 90% scouts
plt.subplot(3,1,3)
# Divided food collected by 1000 to convert from microliters to mL
foods_low = cumfood_clu_m[scout_nums.index(90),perst_vals.index(1),:]/1000
errors_low = cumfood_clu_sd[scout_nums.index(90),perst_vals.index(1),:]/1000
foods_med = cumfood_clu_m[scout_nums.index(90),perst_vals.index(10),:]/1000
errors_med = cumfood_clu_sd[scout_nums.index(90),perst_vals.index(10),:]/1000
foods_high = cumfood_clu_m[scout_nums.index(90),perst_vals.index(20),:]/1000
errors_high = cumfood_clu_sd[scout_nums.index(90),perst_vals.index(20),:]/1000 

plt.errorbar(hours,foods_low,yerr=errors_low,ecolor='0.9',color='cornflowerblue')
plt.errorbar(hours,foods_med,yerr=errors_med,ecolor='0.9',color='blue',linestyle='--')
plt.errorbar(hours,foods_high,yerr=errors_high,ecolor='0.9',color='navy',linestyle=':')
plt.ylim([0,5])
plt.xlabel('Time (hours)')
plt.title('\n90% Scouts')

figname = 'food_collected_by_time_clumped_vert.png'
plt.savefig(figpath+figname, dpi=500, format='png')

## Make barplots comparing how high and low scout colonies differ in total food collected in clumped vs dispersed
# high = 70% scouts, low = 30% scouts, persistence=10
res=['Resources Clumped',' Resources Dispersed']
LI=['Low Scout','High Scout']
tfoodclump = [tfood_clu_m[2,4],tfood_clu_m[6,4]] # resources clumped, low and high scout resp.
tfooddisp = [tfood_dis_m[2,4],tfood_dis_m[6,4]]  # resources dispersed, low and high scout resp.
sqnr = math.sqrt(nr)                             # square root of sample size to convert sd to se
tfoodclumpse = [tfood_clu_sd[2,4]/sqnr,tfood_clu_sd[6,4]/sqnr] # clumped standard errors
tfooddispse = [tfood_dis_sd[2,4]/sqnr,tfood_dis_sd[6,4]/sqnr]  # dispersed standard errors
N=2                   # the number of groups
ind = np.arange(N)    # the x locations for the groups
width = 0.35          # the width of the bars
fig,ax = plt.subplots()
p1 = ax.bar(ind, tfoodclump, width, color='red', yerr=tfoodclumpse)         # clumped bars
p2 = ax.bar(ind+width, tfooddisp, width, color='blue', yerr=tfooddispse)    # dispersed bars
ax.set_xticks(ind + width / 2)
ax.set_xticklabels((LI))
ax.set_ylabel('Total Food Collected')
ax.legend((p1[0], p2[0]), (res))
ax.set_title('Total Food Collected by Scout Number')
plt.show()
figname='food_collected_hilo_cludis.png'
plt.savefig(figpath+figname, dpi=500,format='png')

## Figure 2. Make boxplots comparing how high and low scout colonies differ in total food collected in clumped vs dispersed
# high = 70% scouts, low = 30% scouts, persistence=20
res=['Resources Clumped',' Resources Dispersed']
#LI=['Low Scout','High Scout']
LI=['30% Scouts','70% Scouts']
# when all persistence values are imported, [:,:,4] is persistence 10
# when just 10 and 20 are imported, [:,:,1] is persistence 20
#tfclump = [tfood_clumped[:,2,4],tfood_clumped[:,6,4]] # resources clumped, low and high scout resp.
#tfdisp = [tfood_dispersed[:,2,4],tfood_dispersed[:,6,4]]  # resources dispersed, low and high scout resp.
tfclump = [tfood_clumped[:,2,1],tfood_clumped[:,6,1]] # resources clumped, low and high scout resp.
tfdisp = [tfood_dispersed[:,2,1],tfood_dispersed[:,6,1]]  # resources dispersed, low and high scout resp.
N=2                   # the number of groups
ind = np.arange(N)    # the x locations for the groups
bwidth = 0.35          # the width of the bars
fig,ax = plt.subplots()
p1 = ax.boxplot(tfclump, positions=ind, widths=bwidth, patch_artist=True, boxprops=dict(facecolor="red"),
                flierprops=dict(marker=".")) # clumped boxes
p2 = ax.boxplot(tfdisp, positions=ind+bwidth, widths=bwidth, patch_artist=True, boxprops=dict(facecolor="blue"),
                flierprops=dict(marker=".")) # dispersed boxes
for bplot in (p1, p2):
    plt.setp(bplot['medians'],color='k')
ax.set_xticks(ind + bwidth / 2)
ax.set_xlim([-.3,1.65])
ax.set_xticklabels((LI))
ax.set_ylabel('Total Food Collected (microL)')
ax.legend([p1["boxes"][0], p2["boxes"][0]], ['Clumped', 'Dispersed'], loc='upper right')
plt.show()
figname='Fig2_food_collected_hilo_cludis_pers20.png'
plt.savefig(figpath+figname, dpi=500,format='png')

## Make barplots comparing how much high and low scout colonies visited different quality feeders
# high = 70% scouts, low = 30% scouts, persistence=10
# visits[i,j,k] = [rep,%scouts,persistence]
sqnr = math.sqrt(nr)
visitsclump_loscout = [lowvisits_clu_m[2,4],medvisits_clu_m[2,4],highvisits_clu_m[2,4]]
visitsdisp_loscout = [lowvisits_dis_m[2,4],medvisits_dis_m[2,4],highvisits_dis_m[2,4]]
visitsclump_hiscout = [lowvisits_clu_m[6,4],medvisits_clu_m[6,4],highvisits_clu_m[6,4]]
visitsdisp_hiscout = [lowvisits_dis_m[6,4],medvisits_dis_m[6,4],highvisits_dis_m[6,4]]
# standard error for each group 
vclump_loscout_se = [lowvisits_clu_sd[2,4]/sqnr,medvisits_clu_sd[2,4]/sqnr,highvisits_clu_sd[2,4]/sqnr]
vdisp_loscout_se = [lowvisits_dis_sd[2,4]/sqnr,medvisits_dis_sd[2,4]/sqnr,highvisits_dis_sd[2,4]/sqnr]
vclump_hiscout_se = [lowvisits_clu_sd[6,4]/sqnr,medvisits_clu_sd[6,4]/sqnr,highvisits_clu_sd[6,4]/sqnr]
vdisp_hiscout_se = [lowvisits_dis_sd[6,4]/sqnr,medvisits_dis_sd[6,4]/sqnr,highvisits_dis_sd[6,4]/sqnr]

N=3                   # the number of groups
ind = np.arange(N)    # the x locations for the groups
bwidth = 0.35          # the width of the bars
plt.subplot(1,2,1)
plt.bar(ind, visitsclump_loscout,width=bwidth, color='red',yerr=vclump_loscout_se)
plt.bar(ind+bwidth, visitsdisp_loscout, width=bwidth, color='blue',yerr=vdisp_loscout_se)
plt.xticks(ind + bwidth / 2,['Low','Medium','High'])
plt.ylim([0,840])
plt.ylabel('Number of Forager Visits')
plt.xlabel('Feeder Quality')
plt.legend(['Clumped','Dispersed'])
plt.title('Low Scout Colonies')

plt.subplot(1,2,2)
plt.bar(ind, visitsclump_hiscout, width=bwidth, color='red',yerr=vclump_hiscout_se)
plt.bar(ind+bwidth, visitsdisp_hiscout, width=bwidth, color='blue',yerr=vdisp_hiscout_se)
plt.xticks(ind + bwidth / 2,['Low','Medium','High'])
plt.ylim([0,840])
plt.xlabel('Feeder Quality')
plt.title('High Scout Colonies')
plt.suptitle('Simulated Forager Visits to Each Feeder')
plt.show()

figname='visits_by_quality_scoutnum_dist.png'
plt.savefig(figpath+figname, dpi=500,format='png')

## Figure 3. make boxplots comparing how much high and low scout colonies visited different quality feeders
# high = 70% scouts, low = 30% scouts, persistence=10
# visits[i,j,k] = [rep,%scouts,persistence]
vclump_loscout = [lowvisits_clu[:,2,0],medvisits_clu[:,2,0],highvisits_clu[:,2,0]]
vdisp_loscout = [lowvisits_dis[:,2,0],medvisits_dis[:,2,0],highvisits_dis[:,2,0]]
vclump_hiscout = [lowvisits_clu[:,6,0],medvisits_clu[:,6,0],highvisits_clu[:,6,0]]
vdisp_hiscout = [lowvisits_dis[:,6,0],medvisits_dis[:,6,0],highvisits_dis[:,6,0]]

N=3                   # the number of groups
ind = np.arange(N)    # the x locations for the groups
bwidth = 0.35         # the width of the bars
labels = ['Clumped','Dispersed']

fig, ax = plt.subplots(1,2)
bplot1a = ax[0].boxplot(vclump_loscout, positions=ind, widths=bwidth, patch_artist=True,
            boxprops=dict(facecolor="red"),flierprops=dict(marker='.',markersize=4))
bplot1b = ax[0].boxplot(vdisp_loscout, positions=ind+bwidth, widths=bwidth, patch_artist=True,
            boxprops=dict(facecolor="blue"),flierprops=dict(marker='.',markersize=4))
ax[0].set_xticks(ind + bwidth / 2,)
ax[0].set_xticklabels(['Low','Medium','High'])
ax[0].set_xlim([-.35,2.7])
ax[0].set_ylim([-30,1630])
ax[0].set_ylabel('Number of Visits')
ax[0].set_xlabel('Feeder Quality')
ax[0].set_title('30% Scouts')

bplot2a = ax[1].boxplot(vclump_hiscout, positions=ind, widths=bwidth, patch_artist=True,
            boxprops=dict(facecolor="red"),flierprops=dict(marker='.',markersize=4))
bplot2b = ax[1].boxplot(vdisp_hiscout, positions=ind+bwidth, widths=bwidth, patch_artist=True,
            boxprops=dict(facecolor="blue",hatch="/"),flierprops=dict(marker='.',markersize=4))
ax[1].set_xticks(ind + bwidth / 2)
ax[1].set_xticklabels(['Low','Medium','High'])
ax[1].set_xlim([-.35,2.7])
ax[1].set_ylim([-30,1630])
ax[1].set_xlabel('Feeder Quality')
ax[1].set_title('70% Scouts')
ax[1].legend([bplot2a["boxes"][0], bplot2b["boxes"][0]], ['Clumped', 'Dispersed'], loc='upper right')

# colormap for figure
reds =  [(1,.671,.671),
         (.824,0,0),
         (.706,0,0)]
blues = [(.686,.686,1),
         (.184,.184,1),
         (0,0,.424)] 
        
for bplot in (bplot1a, bplot2a):
    plt.setp(bplot['medians'],color='grey')
    for patch in bplot['boxes']:
        i = bplot['boxes'].index(patch)
        patch.set_facecolor(reds[i])
        
for bplot in (bplot1b, bplot2b):
    plt.setp(bplot['medians'],color='grey')
    for patch in bplot['boxes']:
        i = bplot['boxes'].index(patch)
        patch.set_facecolor(blues[i])
        patch.set_hatch('/')

#plt.suptitle('Simulated Forager Visits to Each Feeder')

figname='visits_by_quality_scoutnum_dist_box.png'
plt.savefig(figpath+figname, dpi=500,format='png')

## Figure 4- food collected as function of scout number for clumped vs dispersed, persistence 20
plot = plt.figure()
ax = plot.add_subplot(111)
ax.errorbar(scout_nums, nfood_clu_m[:,1], yerr=(nfood_clu_sd[:,1]/math.sqrt(nr)),color='red', 
             label='Clumped')
ax.errorbar(scout_nums, nfood_dis_m[:,1], yerr=(nfood_dis_sd[:,1]/math.sqrt(nr)),color='blue', 
             linestyle='--', label='Dispersed')

plt.xlabel('% Scouts')
plt.ylabel('Net Food Collected (microL)')
plt.legend()
plt.text(39.5,3975,'*',color='red')
plt.text(29.5,3975,'*',color='blue')

figname = 'net_food_optimalscouts_prst20.png'
plt.savefig(figpath+figname, dpi=400, format='png')

## Figure 4 with two panels: net food collected and visit number
plot = plt.figure()
ax = plot.add_subplot(121)
ax.errorbar(scout_nums, nfood_clu_m[:,1], yerr=(nfood_clu_sd[:,1]/math.sqrt(nr)),color='red', 
             label='Clumped')
ax.errorbar(scout_nums, nfood_dis_m[:,1], yerr=(nfood_dis_sd[:,1]/math.sqrt(nr)),color='blue', 
             linestyle='--', label='Dispersed')

plt.xlabel('% Scouts')
plt.ylabel('Net Food Collected (microL)')
plt.legend()
plt.text(39.5,3975,'*',color='red')
plt.text(29.5,3975,'*',color='blue')

ax2 = plot.add_subplot(122)
ax2.errorbar(scout_nums, totalvisits_clu_m[:,1], yerr=(totalvisits_clu_sd[:,1]/math.sqrt(nr)),color='red')
ax2.errorbar(scout_nums, totalvisits_dis_m[:,1], yerr=(totalvisits_dis_sd[:,1]/math.sqrt(nr)),color='blue',
             linestyle='--')
ax2.set_ylabel('Total Number of Visits to Feeders')
ax2.set_xlabel('% Scouts')

plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(10,4.72)

figname = 'Fig4_AB.png'
plt.savefig(figpath+figname, dpi=400, format='png')

## Figure 2 with two panels: total food collected and net food collected
# Make boxplots comparing how high and low scout colonies differ in total food collected in clumped vs dispersed
# high = 70% scouts, low = 30% scouts, persistence=20
res=['Resources Clumped',' Resources Dispersed']
#LI=['Low Scout','High Scout']
LI=['30% Scouts','70% Scouts']
# when all persistence values are imported, [:,:,4] is persistence 10
# when just 10 and 20 are imported, [:,:,1] is persistence 20
tfclump = [tfood_clumped[:,2,1],tfood_clumped[:,6,1]] # resources clumped, low and high scout resp.
tfdisp = [tfood_dispersed[:,2,1],tfood_dispersed[:,6,1]]  # resources dispersed, low and high scout resp.
nfclump = [nfood_clumped[:,2,1],nfood_clumped[:,6,1]]
nfdisp = [nfood_dispersed[:,2,1],nfood_dispersed[:,6,1]]

N=2                   # the number of groups
ind = np.arange(N)    # the x locations for the groups
bwidth = 0.35         # the width of the bars

fig = plt.figure()    # make figure

ax = fig.add_subplot(121)  # left axis for total food
p1 = ax.boxplot(tfclump, positions=ind, widths=bwidth, patch_artist=True, boxprops=dict(facecolor="red"),
                flierprops=dict(marker=".")) # clumped boxes
p2 = ax.boxplot(tfdisp, positions=ind+bwidth, widths=bwidth, patch_artist=True, boxprops=dict(facecolor="blue"),
                flierprops=dict(marker=".")) # dispersed boxes
    
ax.set_xticks(ind + bwidth / 2)
ax.set_xlim([-.3,1.65])
ax.set_xticklabels((LI))
#ax.set_ylim([0,5500])
ax.set_ylabel('Total Food Collected (microL)')
ax.legend([p1["boxes"][0], p2["boxes"][0]], ['Clumped', 'Dispersed'], loc='upper right')
#ax.set_title('Total Food Collected by Scout Number')

ax2 = fig.add_subplot(122)  # right axis for net food
p3 = ax2.boxplot(nfclump, positions=ind, widths=bwidth, patch_artist=True, boxprops=dict(facecolor="red"),
                flierprops=dict(marker=".")) # clumped boxes
p4 = ax2.boxplot(nfdisp, positions=ind+bwidth, widths=bwidth, patch_artist=True, boxprops=dict(facecolor="blue"),
                flierprops=dict(marker=".")) # dispersed boxes
ax2.set_xticks(ind + bwidth / 2)
ax2.set_xlim([-.3,1.65])
ax2.set_xticklabels((LI))
ax2.set_ylabel('Net Food Collected (microL)')

for bplot in (p1, p2, p3, p4):
    plt.setp(bplot['medians'],color='k')

fig.set_size_inches(8.5,4.72)
plt.tight_layout()

figname='Fig2AB_food_collected_hilo_cludis_pers20.png'
plt.savefig(figpath+figname, dpi=500,format='png')

## Figure 2 with two panels: total food collected and net food collected
# Make boxplots comparing how high and low scout colonies differ in total food collected in clumped vs dispersed
# high = 70% scouts, low = 30% scouts, persistence=20
res=['Resources Clumped',' Resources Dispersed']
#LI=['Low Scout','High Scout']
LI=['30% Scouts','70% Scouts']
# when all persistence values are imported, [:,:,4] is persistence 10
# when just 10 and 20 are imported, [:,:,1] is persistence 20
nfclump = [nfood_clumped[:,2,1],nfood_clumped[:,6,1]]    # resources clumped, low and high scout resp.
nfdisp = [nfood_dispersed[:,2,1],nfood_dispersed[:,6,1]] # resources dispersed, low and high scout resp.

N=2                   # the number of groups
ind = np.arange(N)    # the x locations for the groups
bwidth = 0.35         # the width of the bars

fig = plt.figure()    # make figure

ax2 = fig.add_subplot(111)
p3 = ax2.boxplot(nfclump, positions=ind, widths=bwidth, patch_artist=True, boxprops=dict(facecolor="red"),
                flierprops=dict(marker=".")) # clumped boxes
p4 = ax2.boxplot(nfdisp, positions=ind+bwidth, widths=bwidth, patch_artist=True, 
                 boxprops=dict(facecolor="blue",hatch="/"),
                flierprops=dict(marker=".")) # dispersed boxes
ax2.set_xticks(ind + bwidth / 2)
ax2.set_xlim([-.3,1.65])
ax2.set_xticklabels((LI))
ax2.set_ylabel('Net Food Collected (microL)')
ax2.legend([p3["boxes"][0], p4["boxes"][0]], ['Clumped', 'Dispersed'], loc='upper right')

for bplot in (p3, p4):
    plt.setp(bplot['medians'],color='k')

plt.tight_layout()

figname='Fig2_netfood_collected_hilo_cludis_pers20.png'
plt.savefig(figpath+figname, dpi=500,format='png')
