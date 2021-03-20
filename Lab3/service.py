from map import Map
from drone import Drone
import random
from constants import Constants

class Service:
    def __init__(self, repository):
        self.__map = Map()
        #self.__map.randomMap()
        #self.__map.saveMap("test1.map")
        self.__map.loadMap("test1.map")
        self.__mapSurface = self.__map.getMapSurface()
        self.__drone = Drone(5, 5) #I'll place it by default on an empty position
        self.__repository = repository
    
    def addNewPopulation(self, populationSize, individualMaxSize, startingCoordinates):
        self.__repository.addNewPopulation(populationSize, individualMaxSize, startingCoordinates, self.__mapSurface)
    
    def getPopulations(self):
        return self.__repository.getPopulations()
    
    def __iteration(self):
        population = self.__repository.getPopulations().pop(0)
        individuals = population.getIndividuals()
        
        firstParentIndex = random.randint(0, len(individuals) - 1)
        secondParentIndex = random.randint(0, len(individuals) - 1)
        while firstParentIndex == secondParentIndex:
            secondParentIndex = random.randint(0, len(individuals) - 1)
        
        firstParent = individuals[firstParentIndex]
        secondParent = individuals[secondParentIndex]
        offspring = firstParent.attemptCrossover(secondParent, Constants.CROSSOVER_PROBABILITY)
        if offspring is None:
            self.__repository.addExistingPopulation(population)
            return # the crossover was not done because it didn't meet the crossover probability
        
        offspring.attemptMutation(Constants.MUTATION_PROBABILITY)
        offspring.computeFitness()
        population.addIndividual(offspring)
        
        self.__repository.addExistingPopulation(population) 
    
    def runGeneration(self):
        for iteration in range(Constants.ITERATIONS_PER_GENERATION):
            self.__iteration()
        population = self.__repository.getPopulations().pop(0)
        population.setIndividuals(population.selection(Constants.POPULATION_SIZE))
        self.__repository.addExistingPopulation(population)
    
    def getMapSurface(self):
        return self.__map.getMapSurface()
    
    def getDroneXCoord(self):
        return self.__drone.getX()
    
    def getDroneYCoord(self):
        return self.__drone.getY()