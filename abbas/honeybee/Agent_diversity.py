"""
Version with diversity of resource qualities. Scouts and recruits will dance for a resource in proportion to its
quality.
Edited 10.18.18, 1.30.2021
"""

import numpy as np
from numpy import linalg as la
import random
from math import *

class HoneyBee:
    """
    mode:
    -3 = Returning to previously visited spot  
    -2 = Dancing, dancing...
    -1 = Explorer returning to hive
     0 = Exploring
     1 = Exploiter waiting
     2 = Exploiter recruited
    """
    
    hiveX = 100 # x coordinate of hive
    hiveY = 100 # y coordinate of hive

    ## Important variables
    timeWagDance = 50                 # Time each bee spends dancing
    #broadcastedPositions = {}        # Broadcasted spots
    Nbees = 0                         # Total number of bees
    #recrutableBees = 0               # Number of bees that can be recruited

    Krecruitment = 0.1                # average recruitment per dancing bee per dt
    # Average number of recruited bee per dance: timeWagDance x Krecruitment / recrutables
    
    
    # Energy consumption parameters: dE = a + b*x**3
    dE_a = 1e-5
    dE_b = 1e-6

    # init is the function executed whenever a new HoneyBee instance is created
    def __init__(self, BeeId, bclass, mode, x0, y0, Lx = 200, Ly = 200, v = 1.5,
                 tsigma = 3., persistence = 5):
        
        self.BeeId = BeeId

        ## Main definitions
        self.x = x0    # bee's x position
        self.y = y0    # bee's y position
        self.bclass = bclass # explorer or exploiter
        self.mode = mode  # current behavior (searching, dancing, etc)
        self.spot = []  # contains coordinates of the resource spot most recently found
        self.load = 0 # contains food concentration of the resource spot most recently visited
        
        ## Direct channel to the Hive, identity of the Hive this bee belongs to
        self.Hive = None
        
        
        ## Keep track of the energy
        self.energy = 0.    # bee's energy expenditure
        
        
        ## Dynamical variables
        self.v = v    # bee's average velocity
        self.v_explore = v
        self.v_exploit = 1.0
        self.tsigma = tsigma   # variance in bee's velocity
        self.tsigma_explore = tsigma
        self.tsigma_exploit = 2.0
        
        self.recruitedSpot = [] # contains coordinates of the spot it has been recruited to by dance
        
        self.wagdance_t = 0
        
        self.persistence = persistence    # persistence = return time
        
        ## Creating an explorer
        if self.bclass == 0:
            self.update    = self.move
            self.updatePos = self.DriftRandomWalk
            self.Returned  = self.explorerReturned

            # Assigning a random exploration vector
            self.new_drift_vector()
            
            self.returnCount = 0

        ## Creating an exploiter
        elif self.bclass == 1:
            #HoneyBee.recrutableBees += 1
            self.update    = self.Recruitment
            self.updatePos = self.exploiterWalk
            self.Returned  = self.exploiterReturned

            self.returnCount = 0
            
        return
    


    ###
    ### Functions to update group parameters
    ###
    
    def updatePersistence(self, RT):
        """Persistence is an individual feature, which shows how persistent a
        given bee is when exploring a given resource spot.
        """
        self.persistence = RT
        return
    
    def updateHivePosition(self, Pos):
        HoneyBee.hiveX = Pos[0]
        HoneyBee.hiveY = Pos[1]
        return
    
    def updateWagDanceDuration(self, T):
        self.timeWagDance = T
        return
    
    def updateHAvgRecruitment(K):
        """This method updates the average number of recruited bees per time
        step for all bees.
        """
        HoneyBee.Krecruitment = K
        return 


    
    ###
    ### Dynamical functions
    ### 
    
    def foundSpot(self):
        """Generic function to update the bee's status when a resource spot is
        found.
        
        Specifically, it will set spot field to the position where the
        spot was found and its mode to -1 (return to the hive).

        """
        self.spot = [int(self.x), int(self.y)] # bee's current position
        self.mode = -1
        return

    
    
    def move(self, scale = 3):
        
        ## Exploring
        if self.mode == 0 or self.mode == -3: 
            self.updatePos()

        ## Found spot, returning home
        elif self.mode == -1:
            
            if int( abs(self.x - self.hiveX) ) < 3 and int( abs(self.y - self.hiveY) ) < 3: 
                self.Returned() # bee is back in hive now
                
            else:
                cons = -.3/sqrt( (self.x - self.hiveX)**2 + (self.y - self.hiveY)**2 ) # dist from bee to hive
                self.x += cons*scale*(self.x - self.hiveX) # move in direction of hive with speed of 1
                self.y += cons*scale*(self.y - self.hiveY)

        ## Dancing, dancing, she's a dancing machine...
        elif self.mode == -2:
            
            self.wagdance_t += 1

            # Stops the dance after a while
            if self.wagdance_t >= self.timeWagDance:
                
                ## Danced enough
                self.wagdance_t = 0
                
                ## Leaving the hive again
                
                # When the scout is about to leave the Hive, it has
                # two options: it may either go back to exploit the
                # same spot or try to explore the evironment.
                
                if self.persistence == 0:
                    # Exploring the environment
                    self.leaveHive(mode = 0) # explores for new resources
                    
                else:
                    # Going back to explore
                    self.leaveHive(mode = -3) # returns again to known spot

                
                ## Stops recruitment, "Hive" is the name of the Forage instance
                self.Hive.broadcastedPositions.pop(self.BeeId)
            

        ## Oops, going too far:
        ## Makes the bee back to the hive safe and sound.
        if abs(self.x - self.hiveX) > self.hiveX or abs(self.y - self.hiveY) > self.hiveX:
            self.x = self.hiveX
            self.y = self.hiveY
            if self.bclass == 0: self.mode = 0
            else: self.mode = 1

        return
    

    def new_drift_vector(self):
        self.v_drift = np.array([random.random() - 0.5, random.random() - 0.5])
        self.v_drift /= la.norm(self.v_drift) # gives bee a speed of 1
        self.theta = acos(self.v_drift[0])*np.sign(self.v_drift[1]) # new movement angle
        return
    

    
    ###
    ### Dynamics when returning to the hive
    ###
    

    def exploiterReturned(self):
        
        if self.returnCount == self.persistence:    # if number of returns so far is equal to bee's persistence, it is done exploiting that spot now
            self.mode = 1                           ## back to state Waiting for recruitments
            self.update = self.Recruitment          ## Available back to recruitment
            self.returnCount = 0
            
        elif self.returnCount == 0:                # if bee has never returned from this spot before
            danciness = self.load * 0.1
            if np.random.rand() < danciness:       # bee will dance with probability that depends on spot quality
                self.mode = -2
                self.broadcastSpot()               # adds the bee's most recently visited spot to colony's array of broadcasted positions
                self.returnCount += 1
            else:
                self.returnCount += 1
                self.leaveHive( mode = -3 )
            
        else:
            self.returnCount += 1                  # bee goes back to visit the last-visited spot again
            self.leaveHive( mode = -3 )
            
                
        ## Undoing any modification
        self.x = self.hiveX  # bee is located at hive again
        self.y = self.hiveY
        self.updatePos = self.exploiterWalk
        
        ## Dropping off our load of food at the hive
        load = self.load
        self.Hive.Log[self.Hive.t,1] += load # add food to the hive when exploiter returns from foraging
        self.load = 0 # now bee is unladen again
        #self.Hive.addFood()   
        
        return

    
    def explorerReturned(self):
        
        if self.returnCount == self.persistence:
            self.leaveHive( mode = 0 )  # back to exploring for new spots
            
        elif self.returnCount == 0:
            danciness = self.load * 0.33           # scouts are more likely to dance than recruits
            if np.random.rand() < danciness:       # bee will dance with probability that depends on spot quality
                self.mode = -2
                self.broadcastSpot()               # adds the bee's most recently visited spot to colony's array of broadcasted positions
                self.returnCount += 1
            else:
                self.returnCount += 1
                self.leaveHive( mode = -3 )
            
        else:
            #self.mode = -3
            self.returnCount += 1
            self.leaveHive( mode = -3 )

        
        self.x = self.hiveX    # bee's position is back at the hive
        self.y = self.hiveY
        
        ## Dropping off our load of food at the hive
        load = self.load
        self.Hive.Log[self.Hive.t,1] += load # add food to the hive when explorer returns from foraging
        self.load = 0 # now bee is unladen again
        #self.Hive.addFood()

        return


    def leaveHive(self, mode = 0):
        """This function sets a scout to start foraging, with a new drifting
        vector.
        
       
        """
        
        self.mode = mode             ## back to state Waiting for recruitments
        self.update = self.move      ## It's going to get back to explore
        
        if self.mode == 0:   # exploring for new resource spots
            
            # Clearing spot memory
            self.spot = []    # forget most recently visited spot
            
            # Making sure this variable is reset to 0.
            self.returnCount = 0
            
            # Restoring the exploring acuity.
            self.v = self.v_explore
            self.tsigma = self.tsigma_explore
            self.updatePos = self.DriftRandomWalk # wandering in random direction
            
            self.v_drift = self.new_drift_vector()  ## Get new drift vector
            self.recruitedSpot = []
            
        elif mode == -3:    # returning to a known resource spot
            # Setting the acuity
            self.v = self.v_exploit
            self.tsigma = self.tsigma_exploit
            self.updatePos = self.exploiterWalk # moving in direction of known resource
            
            # Setting the target
            U = self.spot    # coordinate of last known spot
            self.recruitedSpot = np.array( U )
            u = np.array( U ) - np.array([self.hiveX,self.hiveY])

            mdu = la.norm(u)
            if mdu != 0.:
                self.v_drift = u/la.norm(u)

            self.theta = acos(self.v_drift[0])*np.sign(self.v_drift[1])
            
        return 
    
    

    
    ###
    ### Recruitment and broadcasting spots
    ###
    
    def broadcastSpot(self):
        self.Hive.broadcastedPositions[self.BeeId] = self.spot
        return
    

    
    def Recruitment(self):
        
        if self.Hive.broadcastedPositions:
            
            Pos = np.array(list(self.Hive.broadcastedPositions.values())) # an array of the broadcasted positions

            #if self.Hive.Nexploiters - self.Hive.Nrecruiteds < 0 : print 'ERROR 101 -- Misscounting recruits.'
            if Pos.shape[0] > 0 and random.random() < self.Krecruitment / float( self.Hive.Nexploiters - self.Hive.Nrecruiteds ) :
                #HoneyBee.recrutableBees -= 1
                U = Pos[ np.random.choice( np.arange(Pos.shape[0]), 1 )[0] ] # choose a random spot from the array of broadcasted resource spots
                self.mode = 0
                self.update = self.move
            
                self.recruitedSpot = np.array( U ) # currently known spot is now the one chosen from the array of broadcasted spots
                self.spot = self.recruitedSpot     # this would be a possible place to stick in an option to either recruit to a new spot or return to a previously known spot
                u = np.array( U ) - np.array([self.hiveX,self.hiveY]) # new movement direction is diff. between recruited spot and hive
                try:
                    unorm = la.norm(u)
                    self.v_drift = u/unorm        # off to find new spot we've learned about
                except:
                    print(u)
                    print(vnorm)
                
                self.theta = acos(self.v_drift[0])*np.sign(self.v_drift[1])
            
        return
    
    
    def energyUpdate(self, dx):
        self.energy += (self.dE_a + self.dE_b*dx**3)   # energy expenditure based on distance traveled
        return
    
    
    
    
    ###
    ### Moving Routines
    ###
    
    def stayInHive(self):    # do nothing
        return
    
    def StraightLine(self):
        dx = 1.0 + int( 3*random.random() ) - 1
        dy = int( 3*random.random() ) - 1

        self.x += dx
        self.y += dy
        self.energyUpdate(sqrt(dx**2 + dy**2))
        return
    
    def DriftRandomWalk(self):
        theta = self.theta + self.tsigma*(random.random() - 0.5) # angle of walk = bee's current angle plus random error
        dx = self.v*cos( theta )    # set new x,y vector so bee moves in direction of angle theta
        dy = self.v*sin( theta )
        
        self.x += dx    # bee moves in its new direction
        self.y += dy
        self.energyUpdate(sqrt(dx**2 + dy**2)) # update energy expenditure based on distance moved
        return
    
    def exploiterWalk(self):
        
        trand = np.random.random() #save the random num so we can see it
        theta = self.theta + self.tsigma*(trand - 0.5)
        dx = self.v*np.cos( theta )
        dy = self.v*np.sin( theta )
        
        if isnan(dx):
            print(self.x, self.y, self.BeeId)
            print(self.v, self.theta, self.tsigma, theta, dx, dy)
            print(trand)      
            
        self.x += dx
        self.y += dy
        self.energyUpdate(sqrt(dx**2 + dy**2))
              
        try:
            dist_hive_recruited_spot = la.norm( self.recruitedSpot - np.array([self.hiveX,self.hiveY]) )
            dist_hive_to_bee = la.norm( np.array([int(self.x),int(self.y)]) - np.array([self.hiveX,self.hiveY]) )
            d = dist_hive_recruited_spot - dist_hive_to_bee
        except:
            print(self.x, self.y, self.BeeId)
            print(self.v, self.tsigma, theta, dx, dy)
            print(self.theta + self.tsigma*(trand - 0.5))

        if d < 0: self.updatePos = self.RandomWalkUpdate
                          
        return
    
    def RandomWalkUpdate(self):
        dx = 3*(random.random() - 0.5) # walk around in a random direction until you find something
        dy = 3*(random.random() - 0.5)
        
        self.x += dx
        self.y += dy
        self.energyUpdate(sqrt(dx**2 + dy**2))
        return
