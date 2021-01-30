"""
Version with diversity of resource qualities. Scouts and recruits will dance for a resource in proportion to its
quality. Also edited so we record how many bees visit each type of resource.
Edited 1/24/2021, 1.31.2021
"""

import numpy as np
import pylab as pl
import random
from math import *
from Agent_diversity import HoneyBee

# Each object in class Forage represents one instance of the simulation 
class Forage:
    
    
    def __init__(self, Nexplorer = 5, Nexploiter = 100, T = 1500,
                 SctPersistence = 1, RecPersistence = 5):

        self.NBeesTotal = Nexplorer + Nexploiter
        
        # Area size
        self.Lx = 500
        self.Ly = 500
        
        # Resources        
        #self.Area  = np.zeros( (self.Lx, self.Ly), dtype=int )
        self.Area1 = np.zeros( (self.Lx, self.Ly), dtype=int ) # The landscape of possible resource locations
        self.Area2 = np.zeros( (self.Lx, self.Ly), dtype=int ) # Areas 1, 2, and 3 contain different types of flowers
        self.Area3 = np.zeros( (self.Lx, self.Ly), dtype=int ) # Each area has different quality nectar
        self.RescMax = 50 # the maximum number of resource units that can occur in a single point
        self.Qual2 = 2 # ratio of how much higher quality resource type 2 is than resource type 1
        self.Qual3 = 3 # ratio of how much higher quality resource type 3 is than resource type 1

        
        self.Nexplorers = Nexplorer   # number of scouts in colony
        self.Explorers = []           # list of all explorers in colony
        for BeeId in range(self.Nexplorers):
            self.Explorers.append(    # to make each explorer, create an object in class "honeybee" with scout parameters
                HoneyBee(BeeId, 0, 0,          # mode exploring, bclass scout
                         self.Lx/2, self.Ly/2, # starting location is hive position
                         v = 1.5, tsigma = 5., # scout velocity and error
                         persistence = SctPersistence) # scout persistence
            )
            self.Explorers[-1].Hive = self  # each new bee has an attribute Hive, which is set equal to the name of the Forage instance

        
        self.Nexploiters = Nexploiter
        self.Exploiters = []
        for BeeId in range(self.Nexplorers, self.Nexplorers + self.Nexploiters):
            self.Exploiters.append(
                HoneyBee(BeeId, 1, 1,            # mode waiting, bclass recruit
                         self.Lx/2, self.Ly/2+2, # starting location is hive position, why are these bees starting slightly away from hive?
                         v = 1.0, tsigma = 2.,   # recruit velocity and error
                         persistence = RecPersistence ) # recruit persistence
            )
            self.Exploiters[-1].Hive = self
        
        
        ## Updating location of the hive
        self.Explorers[0].updateHivePosition([self.Lx/2, self.Ly/2])
        self.Nrecruiteds = 0    # initially, no one is recruited yet
        
        print(len(self.Explorers), len(self.Exploiters))
        
        # Broadcasted positions
        # The idea is that scout bees will use this dictionary to broadcast
        # the position of newly found spots to other bees.
        self.broadcastedPositions = {} 
        
        
        #HoneyBee.Hive = self
        # Log is the array storing the outcome variables of interest
        Nfeatures = 8       # adding three coloumns to record number of visits to each type of resource
        # columns 5, 6, 7 will have number of visits to low, med, and high quality resource, respectively
        self.Log = np.zeros( (T, Nfeatures) )
        self.t = 0
        
        return
    
    
    
    
    ### 
    ### Resources distributions
    ### 
    
    #def resourcesPoissonPP(self, fraction = 0.0005, ri = 40.):
    def resourcesPoissonPP(self, Nres, ri = 40.):
        """Spreads resources around the area for the bees to look for. It is
        implemented as a Poisson Point process.

        """
        
        rmax = min(self.Lx, self.Ly)/2 # half the length/width of foraging arena, i.e. the center
        
        N = self.Lx * self.Ly # the total area of the foraging arena

        self.Resx = np.zeros((Nres))    # Nres is total number of resource points, i.e. resource quantity
        self.Resy = np.zeros((Nres))    # each resource point gets an X and Y coordinate
        for j in range(Nres):
            r = (rmax - ri)*random.random() + ri # r is a random distance btwn ri and rmax
                                                 # r is distance of the spot from the hive
            theta = 2*3.1415*random.random() # random angle between 0 and 2pi radians, angle of the spot
            self.Resx[j] = r*sin(theta) + self.Lx/2
            self.Resy[j] = r*cos(theta) + self.Ly/2
            self.Area[self.Resx[j], self.Resy[j]] = int( 5*random.random() )
        
        return
    
    def resourcesPatchy(self, Nr, size = 6, ps = 0.1, ri = 40.):
        """Spreads resources around the area for the bees to look for. The
        resources occur in square patches, randomly positioned.

        """

        twopi = 2*pi
        rmax = min(self.Lx, self.Ly)/2 - size
        self.Resx = np.zeros((Nr))  # x coordinates of resource patches
        self.Resy = np.zeros((Nr))  # y coordinates of resource patches
        
        for j in range(Nr):
            r = (rmax - ri)*random.random() + ri # radius is random num between ri and rmax
            theta = twopi*random.random()  # theta is random angle from 0 to 2pi
            self.Resx[j] = x = r*sin(theta) + self.Lx/2
            self.Resy[j] = y = r*cos(theta) + self.Ly/2

            for j in range(int(x - size), int(x + size)):
                for k in range(int(y - size), int(y + size)):
                    if random.random() <= ps: self.Area[j,k] = int( self.RescMax*random.random() )
        
        return


    
    def resourcesCircleRandom(self, Nr, R, dR, size = 6, ps = 0.1, ri = 40.):
        """Spreads resources around the area for the bees to look for. The
        patches are a fixed distance from the hive in a random direction.

        """
        
        twopi = 2*pi
        self.Resx = np.zeros((Nr))
        self.Resy = np.zeros((Nr))
        
        for j in range(Nr):
            r = dR*(random.random() - 0.5) + R
            theta = twopi*random.random()
            self.Resx[j] = x = r*sin(theta) + self.Lx/2
            self.Resy[j] = y = r*cos(theta) + self.Ly/2

            for j in range(int(x - size), int(x + size)):
                for k in range(int(y - size), int(y + size)):
                    if random.random() <= ps: self.Area[j,k] = int( self.RescMax*random.random() )
        
        return


    def resourcesCircle(self, Nr, R, size = 6, ps = 0.1, ri = 40.):
        """Spreads resources around the area for the bees to look for. The
        resource patches are a fixed distance from the hive and fixed direction.

        """
        
        rmax = min(self.Lx, self.Ly)/2
        self.Resx = np.zeros((Nr))
        self.Resy = np.zeros((Nr))
        
        dTheta = 2*pi/Nr
        theta = 0.
        
        for j in range(Nr):
            theta += dTheta
            self.Resx[j] = x = R*sin(theta) + self.Lx/2
            self.Resy[j] = y = R*cos(theta) + self.Ly/2
            
            for j in range(int(x - size), int(x + size)):
                for k in range(int(y - size), int(y + size)):
                    if random.random() <= ps: self.Area[j,k] = int( self.RescMax*random.random() )
        
        return


    def resourcesDiverse(self, Nr = 1, R = 200, size = 6, ps = 0.1, ri = 40.):
        """Spreads resources around the area for the bees to look for. Three different types of
        resource patches with different qualities (nectar concentrations). Patches
        have a fixed direction and distance from the hive. Patches equally spread out.
        Nr = number of patches of each type, R = distance of patches from hive, size = half width
        of patches, ps = patch density

        """
        
        rmax = min(self.Lx, self.Ly)/2 # center of foraging arena
        self.Resx1 = np.zeros((Nr)) # Nr is the number of patches of each type
        self.Resy1 = np.zeros((Nr)) # each patch gets an X and Y coordinate
        self.Resx2 = np.zeros((Nr)) # x locations of resource type 2
        self.Resy2 = np.zeros((Nr)) # y locations of resource type 2
        self.Resx3 = np.zeros((Nr)) # x locations of resource type 3
        self.Resy3 = np.zeros((Nr)) # y locations of resource type 3
        
        dTheta = 2*pi/(Nr) # angle between adjacent patches of same type, distributed evenly in circle around hive
        theta1 = 0. # starting angle of first type
        theta2 = theta1 + (dTheta/3.) # so patches of different types alternate
        theta3 = theta2 + (dTheta/3.)
        
        for i in range(Nr): # defines the x,y coord of each patch for resource 1
            
            self.Resx1[i] = x = R*sin(theta1) + self.Lx/2
            self.Resy1[i] = y = R*cos(theta1) + self.Ly/2
            
            for j in range(int(x - size), int(x + size)):  # size is 1/2 the length and width of each patch
                for k in range(int(y - size), int(y + size)):
                    if random.random() <= ps: self.Area1[j,k] = int( self.RescMax*random.random() )
                    # each point in the patch has a probability, ps to have resources located there
                    # each occupied point has between 0 and RescMax resource units
            
            self.Resx2[i] = x2 = R*sin(theta2) + self.Lx/2
            self.Resy2[i] = y2 = R*cos(theta2) + self.Ly/2
            
            for j in range(int(x2 - size), int(x2 + size)):  # size is 1/2 the length and width of each patch
                for k in range(int(y2 - size), int(y2 + size)):
                    if random.random() <= ps: self.Area2[j,k] = int( self.RescMax*random.random() )
                    
            self.Resx3[i] = x3 = R*sin(theta3) + self.Lx/2
            self.Resy3[i] = y3 = R*cos(theta3) + self.Ly/2
            
            for j in range(int(x3 - size), int(x3 + size)):  # size is 1/2 the length and width of each patch
                for k in range(int(y3 - size), int(y3 + size)):
                    if random.random() <= ps: self.Area3[j,k] = int( self.RescMax*random.random() )
            
            theta1 += dTheta
            theta2 += dTheta
            theta3 += dTheta
        
        return


    def resourcesDiverseClumped(self, Nr = 1, R = 200, size = 6, ps = 0.1, ri = 40.):
        """Spreads resources around the area for the bees to look for. Three different types of
        resource patches with different qualities (nectar concentrations). Patches
        have a fixed direction and distance from the hive. Patches clumped.
        Nr = number of patches of each type, R = distance of patches from hive, size = half width
        of patches, ps = patch density

        """
        
        rmax = min(self.Lx, self.Ly)/2 # center of foraging arena
        self.Resx1 = np.zeros((Nr)) # Nr is the number of patches of each type
        self.Resy1 = np.zeros((Nr)) # each patch gets an X and Y coordinate
        self.Resx2 = np.zeros((Nr)) # x locations of resource type 2
        self.Resy2 = np.zeros((Nr)) # y locations of resource type 2
        self.Resx3 = np.zeros((Nr)) # x locations of resource type 3
        self.Resy3 = np.zeros((Nr)) # y locations of resource type 3
        
        dTheta = 2*pi/(Nr) # angle between adjacent patches of same type, distributed evenly in circle around hive
        theta1 = 0. - (dTheta/15.)    # starting angle of first type
        theta2 = theta1 + (dTheta/15.) # so patches of different types alternate
        theta3 = theta2 + (dTheta/15.)
        
        for i in range(Nr): # defines the x,y coord of each patch for resource 1
            
            self.Resx1[i] = x = R*sin(theta1) + self.Lx/2
            self.Resy1[i] = y = R*cos(theta1) + self.Ly/2
            
            for j in range(int(x - size), int(x + size)):  # size is 1/2 the length and width of each patch
                for k in range(int(y - size), int(y + size)):
                    if random.random() <= ps: self.Area1[j,k] = int( self.RescMax*random.random() )
                    # each point in the patch has a probability, ps to have resources located there
                    # each occupied point has between 0 and RescMax resource units
            
            self.Resx2[i] = x2 = R*sin(theta2) + self.Lx/2
            self.Resy2[i] = y2 = R*cos(theta2) + self.Ly/2
            
            for j in range(int(x2 - size), int(x2 + size)):  # size is 1/2 the length and width of each patch
                for k in range(int(y2 - size), int(y2 + size)):
                    if random.random() <= ps: self.Area2[j,k] = int( self.RescMax*random.random() )
                    
            self.Resx3[i] = x3 = R*sin(theta3) + self.Lx/2
            self.Resy3[i] = y3 = R*cos(theta3) + self.Ly/2
            
            for j in range(int(x3 - size), int(x3 + size)):  # size is 1/2 the length and width of each patch
                for k in range(int(y3 - size), int(y3 + size)):
                    if random.random() <= ps: self.Area3[j,k] = int( self.RescMax*random.random() )
            
            theta1 += dTheta
            theta2 += dTheta
            theta3 += dTheta
        
        return
    
    
    ### 
    ### Dynamics routines
    ### 
    
    def update(self):
        
        
        ## Updating explorers
        for bee in self.Explorers:
            bee.update()    # update method causes bees to move
            if ( bee.mode == 0 or bee.mode == -3 ):                
                if self.Area3[int(bee.x),int(bee.y)].sum() > 0 :
                    bee.foundSpot()
                    bee.load = self.Qual3
                    self.Log[self.t,0] += 1 # add 1 to number of scouts who found stuff at time t
                    self.Log[self.t,7] += 1 # add 1 to number of visits to Area3 at time t
                    self.Area3[int(bee.x),int(bee.y)] -= 1   # bee removes 1 unit of resource from its found spot
                
                elif self.Area2[int(bee.x),int(bee.y)].sum() > 0 :
                    bee.foundSpot()
                    bee.load = self.Qual2
                    self.Log[self.t,0] += 1
                    self.Log[self.t,6] += 1 # add 1 to number of visits to Area2 at time t
                    self.Area2[int(bee.x),int(bee.y)] -= 1   # bee removes 1 unit of resource from its found spot
                    
                elif self.Area1[int(bee.x),int(bee.y)].sum() > 0 :
                    bee.foundSpot()
                    bee.load = 1
                    self.Log[self.t,0] += 1 # First column of Log is how many scouts found food at that time
                    self.Log[self.t,5] += 1 # add 1 to number of visits to Area1 at time t
                    self.Area1[int(bee.x),int(bee.y)] -= 1   # bee removes 1 unit of resource from its found spot

            # 3rd column records the energy expenditure of all scouts at time t
            self.Log[self.t, 2] += bee.energy

        
        ## Updating exploiters
        Nrecruiteds_tmp = 0
        for bee in self.Exploiters:
            bee.update()
            if ( bee.mode == 0 or bee.mode == -3 ) :
                if self.Area3[int(bee.x),int(bee.y)].sum() > 0 :
                    bee.mode = -1
                    bee.load = self.Qual3
                    self.Area3[int(bee.x),int(bee.y)] -= 1
                    self.Log[self.t,7] += 1 # add 1 to number of visits to Area3 at time t
                    
                elif self.Area2[int(bee.x),int(bee.y)].sum() > 0 :
                    bee.mode = -1
                    bee.load = self.Qual2
                    self.Area2[int(bee.x),int(bee.y)] -= 1
                    self.Log[self.t,6] += 1 # add 1 to number of visits to Area2 at time t
               
                elif self.Area1[int(bee.x),int(bee.y)].sum() > 0 :
                    bee.mode = -1
                    bee.load = 1
                    self.Area1[int(bee.x),int(bee.y)] -= 1
                    self.Log[self.t,5] += 1 # add 1 to number of visits to Area1 at time t
                    
            # 4th column of Log file is the energy expenditure of all recruits at time t   
            self.Log[self.t, 3] += bee.energy
            if bee.mode <= 0 : Nrecruiteds_tmp += 1 # number of recruited bees at time step
        
        
        ## Keeping track of the number of recruitable bees
        self.Nrecruiteds = Nrecruiteds_tmp
        # Log column 5 is the percent of exploiters that are actively recruited
        self.Log[self.t, 4] = float( self.Nrecruiteds ) / self.Nexploiters
        
        
        self.t += 1
        return
    
    # Log file 2nd column is total food collected by all the foragers at time t
    def addFood(self):
        self.Log[self.t,1] += 1
        return
    
    
    def picture(self, hl0, hle0, hl1):
        
        x = []
        y = []
        for bee in self.Exploiters:
            x.append(bee.x)
            y.append(bee.y)
        hl0.set_xdata(x)
        hl0.set_ydata(y)
        
        x = []
        y = []
        for bee in self.Explorers:
            x.append(bee.x)
            y.append(bee.y)
        hle0.set_xdata(x)
        hle0.set_ydata(y)
        
        x = np.nonzero( self.Area1 )
        hl1.set_xdata( x[0] )
        hl1.set_ydata( x[1] )
        
        return



