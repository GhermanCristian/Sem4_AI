from random import random
from constants import Constants
import numpy as np

class Gene:
    def __init__(self):
        # random initialise the gene according to the representation
        pass

class Individual:
    def __init__(self, maxSize, startingCoordinates):
        self.__maxSize = maxSize
        self.__startingCoordinates = startingCoordinates
        self.__initialiazeChromosome()
        self.__fitness = None
        
    def __initialiazeChromosome(self):
        #self.__chromosome = [Gene() for i in range(self.__size)]
        #generate a random path of length maxSize, starting from that point
        pass
        
    def computeFitness(self):
        # compute the fitness for the individual and save it in self.__fitness
        pass
    
    def attemptMutation(self, mutateProbability):
        if random() < mutateProbability:
            pass # perform a mutation with respect to the representation
    
    def attemptCrossover(self, otherParent, crossoverProbability):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size) 
        if random() < crossoverProbability:
            pass # perform the crossover between the self and the otherParent 
        
        return offspring1, offspring2
    
class Population():
    def __init__(self, populationSize, individualMaxSize, startingCoordinates):
        self.__populationSize = populationSize
        self.__individuals = [Individual(individualMaxSize, startingCoordinates) for x in range(populationSize)]
        
    def evaluate(self):
        # evaluates the population
        for x in self.__individuals:
            x.computeFitness()
            
    def selection(self, k):
        # perform a selection of k individuals from the population and returns that selection
        pass