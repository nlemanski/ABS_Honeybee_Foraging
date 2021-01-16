# Agent Based Simulation of Collective Foraging in Honeybees

To examine how the spatial distribution of resources interacts with individual variation in behavior to shape collective foraging 
decisions, we developed a a spatially-explicit Agent-Based Model. This model is an extension of a previous model called ABBAS 
(Animal Behavior Based on Agents Simulations), the details of which can be found [here](https://github.com/thmosqueiro/ABBAS).

This model simulates honey bees foraging in a two dimensional space containing food patches with three different qualities. These 
food patches can be arranged in two alternative distributions: clumped and dispersed. The model implements detailed flight dynamics
based on a stochastic diffusion processes, parametrized following a wide range of experiments (see below for more details), and a
recruitment mechanism that mimics the [waggle dance in honey bees](https://en.wikipedia.org/wiki/Waggle_dance). Foragers were 
divided into two groups, scouts and recruits, with each group having their own properties.

Using this model we examined how the behavioral composition of the colony (number of scouts) interacts with landscape structure to
influence the colony's collective choice of which resource patches to exploit. Our results are described in a paper currently under
review. The preprint of this paper is available on [BioRxiv ](https://www.biorxiv.org/content/10.1101/817270v1).

#### We also [provide here](https://github.com/nlemanski/ABS_Honeybee_Foraging/ODD.md) a description of the model using the Overview, Design concepts, and Details (ODD) protocol.
