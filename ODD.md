# ODD: Agent-based simulation of a honey bee colony foraging on different landscapes

This description of our model follows the Overview, Design Concepts and Details (ODD) protocol, as presented in Grimm et al. (2020). Parts of this model description are adapted from a previous ODD (Mosqueiro et al., 2017), available here.
The model was implemented using Python v.2.7. The source code of our model implementation can be found on Github. Because we used Python and popular libraries (such as numpy, pylab and math), the core of this implementation is independent of platform and should run on most computers with Python.

## Purpose
The purpose of this model is to examine how the spatial distribution of resources in the environment interacts with individual variation in behavior to shape collective foraging decisions. The model is intended to both reproduce observed patterns of collective behavior in honey bees and to generate new hypotheses for empirical studies of the interaction between individual variation in behavior and landscape structure in shaping collective decision making in honey bees.

Specifically, the goals of the model are to 1) reproduce the emergent pattern of a colony collectively choosing among food patches of different qualities, based on quality-based differences in recruitment, 2) develop predictions about how the spatial distribution of food resources influences a colony’s collective choice of food patches, 3) develop predictions about how the behavioral composition of the colony influences the colony’s collective choice of food patch, and 4) develop predictions about trade-offs between a colony’s ability to locate food patches and its ability to selectively exploit the highest quality patches.

This model was designed for ecologists, behavioral biologists, and computational biologists interested in the effect of environmental features on emergent collective behaviors, such as the foraging behavior of honey bees and other social animals. We detail the model below to allow anyone with basic knowledge of agent-based modelling to reproduce our code in Python or re-implement our model in a language of their choice.

## Entities, state variables, and scales

### Space
Space is represented as a square, two-dimensional landscape, with the hive positioned at the center. Agents may move anywhere within this landscape, however when an agent reaches the edge of the grid, it is transported immediately back to the hive.
The positions of food resources are stored as cells in a 500 by 500 square grid. Within this grid, food resources are aggregated into three square patches. Each patch has a different quality, defined as the number of food units a forager brings back to the hive when it collects a foraging load within that patch. These food patches can be arranged in two alternative distributions: clumped or dispersed. In the dispersed distribution, the three resource patches are evenly spaced in a circle around the hive. In the clumped distribution, all three resource patches are adjacent but not overlapping (Figure S2).

### Model agents
The agents in the model represent honey bee foragers. The agents are divided into two basic types with different behavioral rules: scouts and recruits. Scouts spontaneously leave the hive and explore the environment. Once a scout discovers and exploits a food patch, the scout has a certain probability to report the location and quality of the patch to recruits upon returning to the hive. Recruits remain in the hive until another forager shares the location of a food patch and then have a certain probability to leave the hive to exploit that food patch. After exploiting a food patch, recruits also have a certain probability to report the patch’s location to additional recruits.

### Agent attributes
Each agent in the model has the following attributes:
	Forager type (static): 
Each agent is permanently classified as either a scout or a recruit.
	Forager ID (static):
Each agent is permanently assigned a number, between 1 and 100, as their identity. This number determines the order in which agents are updated at each time step.
	Spatial position (dynamic): 
Each agent has a spatial position, given by a vector (x,y). The position is measured with respect to the hive, located at position (0,0).
	Drifting vector (dynamic): 
Each agent has a drifting vector, which defines the agent’s preferred direction of movement after leaving the hive. An agent’s actual movement is determined by its drifting vector plus a random error term.
	Patch memory (dynamic): 
Each agent stores the location of the food patch they have most recently visited. The location of the stored food patch is given by a vector (x,y).
	Foraging load (dynamic):
Each agent stores the food quality of the patch they have most recently visited, as an integer, from 1-3, increasing with quality.
	Behavioral mode (dynamic): 
Agents classified as scouts move between four different behavioral modes, 1) searching for a new food patch, 2) returning to a previously visited patch, 3) returning to the hive, and 4) recruiting other foragers to a food patch. 
Agents classified as recruits move between five different behavioral modes, 1) waiting to be recruited, 2) searching for an advertised patch, 3) returning to a previously visited patch, 4) returning to the hive, and 5) recruiting other foragers to a food patch.
	Velocity (dynamic):
Each agent has a velocity, which defines how far the agent moves per time step. This velocity is set to 1.5 spatial units per time step when a forager is searching for a new food patch and set to 1 spatial unit per time step when a forager is returning to a previously visited patch.
	Movement error (dynamic):
Each agent has a movement error, which determines the magnitude of the random deviation from the agent’s drifting vector. The movement error is set to 5 when a forager is searching for a new food patch and set to 2 when a forager is returning to a previously visited patch.
	Return count (dynamic):
Each agent has a return count (an integer), which tracks the number of times the forager has visited its most recently visited food patch.
	Elapsed dancing time (dynamic):
When a forager is in the behavioral mode, “recruiting other foragers,” its elapsed dancing time tracks the number of time steps it has spent recruiting so far.

### Global state variables
The environment has the following global state variables that are updated throughout the simulation:
	Time (dynamic):
Time is modeled in discrete steps.
	Food collected (dynamic):
The cumulative number of food units collected by all foragers in the colony.
	Energy expenditure (dynamic):
The cumulative energy expended by all foragers in the colony.
	Patch visits (dynamic):
The cumulative number of times each patch has been visited by a forager.
	Patches found (dynamic):
The cumulative number of scouts that have found food.
	Recruited bees (dynamic):
The number of recruits that are currently exploiting a food patch and unavailable to be recruited.
	Proportion recruited (dynamic):
Proportion of all recruits that are currently exploiting a food patch and unavailable to be recruited.
	Broadcasted positions (dynamic):
The set of all locations that are currently being recruited to, expressed as an array of vectors.

### Scale
Each side of the two-dimensional model landscape is 36 m long, for a total area of 1.3 km2. Each unit of space is approximately 72 cm.
Each unit of time in the simulation represents approximately 1.2 seconds. The simulation was run for 21000 time steps, representing approximately 7 hours of simulated time.
On each foraging trip, a forager collects 1 foraging load, equivalent to 0.1 mL of nectar. Depending on the patch quality, 1 foraging load contains 1, 2, or 3 units of food; 1 unit of food is equivalent to approximately 34 mg sucrose.

## Process overview and scheduling
At model initiation, the location, sizes, and qualities of the food patches are defined using the “resource landscape” submodel and 100 foragers are created using the “create forager” submodel. To determine the order in which agents will act, each forager is assigned an arbitrary forager ID from 1 to 100.
At each time step, the model processes are executed in the following order:
	The scout with the lowest forager ID executes its “update scout” submodel:
	If the scout is in behavioral mode “searching for a new patch” or “returning to a previously visited patch,” it executes the “update position” submodel, in which its position is updated
	If the scout is in behavioral mode “returning to the hive”:
	If its position is equal to (0,0), it executes submodel “scout returned”
	If its position is not equal to (0,0), it moves 1 spatial unit closer to the hive
	If the scout is in behavioral mode “recruiting other foragers”:
	The scout adds 1 to its elapsed dancing time
	If the scout’s elapsed dancing time ≥ the total dancing time parameter, tr, the elapsed dancing time is set to 0, the scout executes the “leave hive” submodel, and the scout’s patch memory vector is removed from the list of broadcasted positions
	If the scout’s position is outside the maximum boundaries of the landscape, the scout’s position is reset to (0,0) and its behavioral mode is set to “searching for a new patch.”
	If the scout has found food, it:
	Executes its “found spot” submodel in which it:
	Updates its patch memory to its current position
	Sets its behavioral mode to “returning to the hive”
	Updates its foraging load
	Updates the state variable patches found
	Adds 1 to the state variable patch visits
	Removes 1 foraging load from its current position in the landscape
	The scout updates the state variable energy expenditure.
	Steps 1-3 are repeated for all remaining scouts, in ascending order of forager ID.
	The recruit with the lowest forager ID executes its “update recruit” submodel:
	If the behavioral mode is “waiting to be recruited,” the recruit executes the “recruitment” submodel.
	If the behavioral mode is “searching for an advertised patch” or “returning to a previously visited patch,” it executes the “update position” submodel in which its position is updated.
	If the behavioral mode is “recruiting other foragers”:
	The recruit adds 1 to its elapsed dancing time
	If the recruit’s elapsed dancing time ≥ the total dancing time parameter, tr, the recruit’s elapsed dancing time is set to 0, the recruit’s patch memory vector is removed from the list of broadcasted positions, and:
	If the recruit’s return count ≥ the persistence parameter, the recruit’s behavioral mode is set to “waiting to be recruited”
	If the recruit’s return count < the persistence parameter, the recruit’s behavioral mode is set to “returning to a previously visited patch”
	If the behavioral mode is “returning to the hive”:
	If its position is equal to (0,0), it executes submodel “recruit returned”
	If its position is not equal to (0,0), it moves 1 spatial unit closer to the hive
	If the recruit’s position is outside the maximum boundaries of the landscape, the recruit’s position is reset to (0,0).
	If the recruit has found food, it:
	Changes its behavioral mode to “returning to the hive”
	Updates its foraging load
	Removes 1 foraging load from its current position in the landscape
	Adds 1 to the state variable patch visits
	The recruit updates the state variable energy expenditure.
	Steps 5-7 are repeated for all remaining recruits, in ascending order of forager ID.
	The state variable recruited bees is set equal to the number of recruits that are in behavioral mode “searching for an advertised food patch,” “returning to a previously visited patch,” or “returning to the hive.”
	The global state variable proportion recruited is updated. Proportion recruited is equal to recruited bees divided by the total number of recruits.

## Design concepts

### Basic principles
This model explores the interaction between the behavioral composition of the colony and the spatial distribution of food resources in determining the colony’s ability to locate food patches and choose among patches with different qualities and different distributions. The two types of foragers (scouts and recruits) perform different tasks. Scouts explore the environment randomly to locate new food patches. Once a patch is discovered, scouts may share the direction, distance, and quality of the food patch with recruits and then return to exploit the patch a fixed number of times. When a scout shares the location of a patch with a recruit, the recruit sets its drifting vector to that location and flies until it finds the advertised resource. After visiting a food patch, recruits may share the direction, distance, and quality of the patch with other recruits, then return to exploit the patch a fixed number of times.  Our model captures the process of how honey bee foragers communicate about food resources using the waggle dance language and incorporates flight behaviors similar to those observed in the field.

### Adaptation
Recruits and scouts that are returning to a particular resource location have lower dispersion than that of scouts exploring the environment. This difference is because bees that are exploiting a resource patch are familiar with its location, and thus faster and more precise than those that are exploring the environment. This change in flight precision increases the chance of a forager finding new resources when exploring the environment, while also increasing the chance of a forager returning to the same location with available resources.

### Prediction
No predictive models were employed in the decision-making processes involved in our model. For instance, recruits decide to leave the hive randomly; foragers decide to stop exploiting resources according to their persistence, which is a fixed constant.

### Sensing
When a forager reports to other recruits the location of a resource patch, recruits that decide to leave the hive and exploit that patch perceive the location of the patch. Once a forager is within 1 unit of distance (~72cm) from a resource, it is able to sense it and, therefore, obtain 1 foraging load of food.

### Interaction
Foragers only interact with each other during the recruitment process at the hive. When one forager recruits another forager to a food patch, the recruit changes its drifting vector to the reported location of the food patch.

### Stochasticity
There are four stochastic elements in this model: creation of resources patches in the environment, assignment of scout drifting vectors, forager flight dynamics, and which advertised resources patches recruits decide to exploit.
	Creation of resources patches: The environment is created with a stochastic process. In all model scenarios, we use an environment with three patches of resources, equally distant from the hive. Each cell within a resource patch contains a stochastic number of resource units, from 0-50.
	Assignment of scout drifting vectors: The angle of the drifting vector of a scout was assigned from a uniform distribution between 0 and 2pi. Because the drifting vector of a forager defines its preferred direction of flight, scouts were equally likely to leave the hive in any direction. The magnitude of the vector was always the same to produce the same average velocity for all foragers.
	The flight dynamics of each forager follow a diffusion process. This diffusion process is usually referred to as a Wiener process, which is a particular case of a Random Walk. On top of this diffusion process, foragers had a preferred direction of movement determined by their drifting vectors.
	Recruits stochastically decide which recruiting forager to follow, with the probability of following any given forager proportional to the quality of the patch they advertise.

### Collectives
All foragers in each simulation belong to a single colony. Foraging performance is calculated as the total amount of resources collected by all foragers in the colony.

### Observation
The data collected from the model are:
	The total amount of food collected by all foragers at each time step
	The total amount of food collected from each of the three patches at each time step
	The total number of times each of the three patches is visited by a forager
	The total energy expended by all foragers at each time step
	The proportion of recruits that are actively recruited at each time step

## Initialization

### Simulation parameters
The simulation is run for 21000 time steps. We run each model scenario 150 times.

### Resource landscape
To initialize the resource landscape in which the colony forages, we execute the submodel “resource landscape”, which defines the locations of three food patches on a two dimensional 500 x 500 square grid with the hive at the center (Figure S2). Each food patch is 40 x 40 units long (5.76 m), with the center located 200 units (14.4 m) from the hive. Within each food patch, the exact location of food is determined by a Poisson point process. Each point has a 0.6 probability to contain resources and each occupied point contains between 0 and 40 foraging loads, drawn from a uniform distribution.
We simulate two different model scenarios: one in which the three resource patches are clumped and one in which they are equally dispersed. In the dispersed scenario, the three patches are 120° from each other, relative to the hive. In the clumped scenario, the three patches are 24° from each other, relative to the hive.

### Colony
At the start of the simulation, we create 100 foragers using the submodel “create forager”. Each forager is assigned a unique forager ID from 1 to 100. When each forager is created, its position is set to the hive (0,0), its patch memory is an empty vector, and its foraging load is set to 0. For all foragers, elapsed dancing time and return count are set to 0.
When a forager is created, its forager type is set to either scout or recruit and does not change throughout the simulation. To explore how the colony’s behavioral composition affects collective foraging decisions, we ran the simulation with 10, 20, 30, 40, 50, 60, 70, 80, or 90 foragers set as scouts.
For scouts, the variable behavioral mode is set to “exploring,” while for recruits, the behavioral mode is set to “waiting to be recruited.” For scouts, initial velocity is set to 1.5 and movement error is set to 5. For recruits, initial velocity is set to 1 and movement error is set to 2. Each scout is assigned a random drifting vector, (x,y), by drawing an angle from a uniform distribution between 0 and 2pi. For recruits, the initial drifting vector is an empty vector.

### Global state variables
The variables food collected, energy expenditure, patch visits, patches found, recruited bees, and proportion recruited are set to 0. The variable broadcasted positions is an empty array.

## Input data
The model does not use any input data to represent time-varying processes. Model dynamics are driven entirely by the initial conditions and stochastic events.

## Submodels
See Table 1 for full list of parameter values.

### Resource landscape
Generates the resource landscape in which the colony forages (Figure S2).
	The landscape consists of three 2-dimensional grids, each defining the location of one of the three food patches. 
	Patch 1 contains high quality food
	Patch 2 contains medium quality food
	Patch 3 contains low quality food
	Each patch has x and y coordinates, which define the patch’s center.
	The model can have two alternate types of resource landscape, where d is the distance from the hive to each patch center (200 spatial units):
	For the evenly dispersed landscape:
	The coordinates (x,y) of patch 1 are (d sin⁡〖(0)〗,d cos⁡〖(0〗 ))
	The coordinates of patch 2 are (d sin⁡〖(2π/3〗), d cos⁡〖(2π/3〗))
	The coordinates of patch 3 are (d sin⁡〖(4π/3〗), d cos⁡〖(4π/3〗))
	For the clumped landscape:
	The coordinates (x, y) of patch 1 are  (d sin⁡〖(-2π/15〗),d cos⁡〖(-2π/15〗))
	The coordinates of patch 2 are (d sin⁡(0),d cos⁡〖(0〗 ))
	The coordinates of patch 3 are (d sin⁡〖(2π/15〗), d cos⁡〖(2π/15〗))
	The length and width of each patch (parameter c) is 40 spatial units. 
	Within each patch, the exact location of food is determined by a Poisson point process:
	Each cell within the patch has a 0.6 probability to contain food (parameter p).
	Cells with food are assigned between 1 and 50 foraging loads, drawn from a uniform distribution.

### Create forager
	Each forager is assigned a unique forager ID, between 1 and 100, to determine the order in which the agents act. 
	Each forager has an initial x and y position of (0,0), the location of the hive. 
	Each forager’s initial foraging load, elapsed dancing time, and return count are set to 0 and initial patch memory is set to an empty vector. 
	Each forager’s persistence (the number of times they return to a patch) is set to 20. 
	Each forager is assigned a forager type of scout or recruit:
	For scouts:
	The initial behavioral mode is set to “searching for a new food patch.” 
	The initial velocity is 1.5 and the initial movement error is 5.
	For recruits:
	The initial behavioral mode is set to “waiting to be recruited.”
	The initial velocity is 1 and the initial movement error is 2.

### Update scout
	If a scout is in behavioral mode “searching for a new food patch” or “returning to a previously visited patch”:
	The scout executes submodel “update position.”
	If the scout is in behavioral mode “returning to the hive”:
	If the scout’s position is within 3 spatial units of the hive, the scout executes submodel “scout returned.”
	If the scout’s position is not within 3 spatial units of the hive, the position is moved one spatial unit closer to the hive.
	If the scout is in behavioral mode “recruiting other foragers”
	The scout adds 1 to the elapsed dancing time.
	If the elapsed dancing time is ≥ tr (the total dancing time):
	The elapsed dancing time is set to 0.
	If the return count ≥ persistence, the behavioral mode is set to “searching for a new food patch.”
	If the return count < persistence, the behavioral mode is set to “returning to a previously visited patch.”
	The scout executes the “leave hive” submodel.
	The scout’s patch memory is removed from the set of broadcasted positions.
	If the scout’s x or y position is > 250 spatial units from the hive:
	The position is set to (0,0).
	If the behavioral mode is not “searching for a new patch,” the behavioral mode is set to “returning to a previously visited patch.”

### Update recruit
	If the recruit’s behavioral mode is “waiting to be recruited”:
	The recruit executes the submodel “recruitment.”
	If the recruit’s behavioral mode is “searching for an advertised patch” or “returning to a previously visited patch”:
	The recruit executes submodel “update position.”
	If the recruit is in behavioral mode “returning to the hive”:
	If the recruit’s position is within 3 spatial units of the hive, the recruit executes submodel “recruit returned.”
	If the recruit ‘s position is not within 3 spatial units of the hive, the position is moved one spatial unit closer to the hive.
	If the recruit is in behavioral mode “recruiting other foragers”:
	The recruit adds 1 to the elapsed dancing time.
	If the elapsed dancing time is ≥ tr (the total dancing time):
	The elapsed dancing time is set to 0.
	If the return count ≥ persistence, the behavioral mode is set to “waiting to be recruited.”
	If the return count < persistence, the behavioral mode is set to “returning to a previously visited patch.”
	The recruit executes the “leave hive” submodel.
	The recruit’s patch memory is removed from the set of broadcasted positions.
	If the recruit’s x or y position is > 250 spatial units from the hive:
	The position is set to (0,0).

### Update position
	If the behavioral mode is “searching for a new patch”:
	A random number, n, is drawn from a uniform distribution between -0.5 and 0.5.
	The forager is assigned a movement angle, θ, equal to their movement error * n + the angle of their drifting vector.
	The forager’s x position increases by velocity * cos(θ).
	The forager’s y position increases by velocity * sin(θ).
	The global variable energy expenditure is increased by dE where:

dE=a+dx^3
and
dx=√((velocity cos(θ))^2+(velocity*sin(θ))^2 )
	If the behavioral mode is “searching for an advertised patch” or “returning to a previously visited patch” and the current position – the drifting vector > 0:
	A random number, n, is drawn from a uniform distribution between -0.5 and 0.5.
	The forager is assigned a movement angle, θ, equal to their movement error * n + the angle of their drifting vector.
	The forager’s x position increases by velocity * cos(θ).
	The forager’s y position increases by velocity * sin(θ).
	The global variable energy expenditure is increased by dE where: 

dE=a+dx^3
and
√((velocity cos(θ))^2+(velocity*sin(θ))^2 )
	If the behavioral mode is “searching for an advertised patch” or “returning to a previously visited patch” and the current position – the drifting vector ≤ 0:
	The change in x position, dx = 3 * a random number between -0.5 and 0.5
	The change in y position, dy = 3 * a random number between -0.5 and 0.5
	The global variable energy expenditure is increased by: √(〖dx〗^2+〖dy〗^2 )

### Scout returned
	If the scout’s return count ≥ persistence:
	The behavioral mode is set to “searching for a new patch.”
	The return count is set to 0.
	If the scout’s return count = 0, the scout begins recruiting with a probability of 0.33 x foraging load.
	If the scout begins recruiting:
	The scout’s behavioral mode is set to “recruiting other foragers.”
	The scout’s patch memory is added to the set of broadcasted positions.
	If the scout does not begin recruiting:
	The behavioral mode is set to “returning to a previously visited patch.”
	The scout executes the submodel “leave hive.”
	The scout’s return count increases by 1.
	If the scout’s return count < persistence but > 0:
	The behavioral mode is set to “returning to a previously visited patch.”
	The scout’s return count increases by 1.
	The scout executes the submodel “leave hive.”
	The scout’s position is set to (0,0).
	The global variable food collected is increased by the scout’s foraging load.
	The scout’s foraging load is set to 0.

### Recruit returned
	If the recruit’s return count ≥ persistence:
	The behavioral mode is set to “waiting to be recruited.”
	The return count is set to 0.
	If the recruit’s return count = 0, the recruit begins recruiting with a probability of 0.1 x foraging load.
	If the recruit begins recruiting:
	The recruit’s behavioral mode is set to “recruiting other foragers.”
	The recruit’s patch memory is added to the set of broadcasted positions.
	If the recruit does not begin recruiting:
	The behavioral mode is set to returning to a previously visited patch.
	The recruit executes the submodel “leave hive.”
	The recruit’s return count increases by 1.
	If the recruit’s return count < persistence but > 0:
	The behavioral mode is set to “returning to a previously visited patch.”
	The recruit’s return count increases by 1.
	The recruit executes the submodel “leave hive.”
	The recruit’s position is set to (0,0).
	The global variable food collected is increased by the recruit’s foraging load.
	The recruit’s foraging load is set to 0.

### Leave hive
	If the forager’s behavioral mode is set to “searching for a new patch”:
	The patch memory is set to an empty vector.
	The return count is set to 0.
	The velocity is set to 1.5.
	The movement error is set to 5.
	The forager is assigned a new drifting vector, (x,y), by drawing an angle from a uniform distribution between 0 and 2pi.
	If the forager’s behavioral mode is set to “returning to a previously visited patch”:
	The velocity is set to 1.
	The movement error is set to 2.
	The drifting vector is set equal to the patch memory vector divided by the norm of the patch memory vector.

### Found spot
	When a forager’s position is within 1 spatial unit of a cell that contains food:
	The forager’s behavioral mode changes to “returning to the hive.” 
	The forager’s patch memory is set equal to the forager’s current position.
	The forager’s foraging load is set equal to the quality of the most recently visited patch.

### Recruitment
	If the set of broadcasted positions contains at least one location vector, the recruit is activated with probability equal to 0.1 / the number of recruits in behavioral mode “waiting to be recruited.”
	If the recruit is activated:
	Its behavioral mode is set to “searching for an advertised food patch.”
	Its patch memory is set equal to a vector from the set of broadcasted positions. The probability of choosing each vector is proportional to the quality, q, associated with that location.
	Its drifting vector is set to equal to the recruited position divided by the norm of the recruited position.

## References

Grimm, V., Railsback, S. F., Vincenot, C. E., Berger, U., Gallagher, C., Deangelis, D. L., … Ayllón, D. (2020). The ODD protocol for describing agent-based and other simulation models: A second update to improve clarity, replication, and structural realism. Journal of Artificial Societies and Social Simulation, 23(2). https://doi.org/10.18564/jasss.4259

Mosqueiro, T., Cook, C., Huerta, R., Gadau, J., Smith, B., & Pinter-Wollman, N. (2017). Task allocation and site fidelity jointly influence foraging regulation in honeybee colonies. Royal Society Open Science, 4(8). https://doi.org/10.1098/rsos.170344

