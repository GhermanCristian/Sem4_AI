from domain.map import Map
from domain.drone import Drone
import random
from constants import Constants
import numpy as np

from domain.pathFixer import PathFixer
from domain.population import Population


class Service:
    def __init__(self, repository):
        self.__map = Map()
        # self.__map.randomMap()
        # self.__map.saveMap("test1.map")
        self.__map.loadMap("test1.map")
        self.__mapSurface = self.__map.getMapSurface()
        self.__drone = Drone(5, 5)  # this is the default position; if occupied => change it
        self.__placeDroneOnEmptyPosition()
        self.__repository = repository

    def __placeDroneOnEmptyPosition(self):
        crtX, crtY = self.__drone.getX(), self.__drone.getY()
        while self.__mapSurface[crtX][crtY] == Constants.WALL_POSITION:
            crtX, crtY = random.randint(0, Constants.MAP_HEIGHT), random.randint(0, Constants.MAP_WIDTH)
        self.__drone.setX(crtX)
        self.__drone.setY(crtY)

    def __iteration(self, population):
        individuals = population.getIndividuals()

        firstParentIndex = random.randint(0, len(individuals) - 1)
        secondParentIndex = random.randint(0, len(individuals) - 1)
        while firstParentIndex == secondParentIndex:
            secondParentIndex = random.randint(0, len(individuals) - 1)

        firstParent = individuals[firstParentIndex]
        secondParent = individuals[secondParentIndex]
        offspring = firstParent.attemptCrossover(secondParent, Constants.CROSSOVER_PROBABILITY)
        if offspring is None:
            return  # the crossover was not done because it didn't meet the crossover probability

        offspring.attemptMutation(Constants.MUTATION_PROBABILITY)
        offspring.computeFitness()
        population.addIndividual(offspring)

    def __runGeneration(self, population):
        for iteration in range(Constants.ITERATIONS_PER_GENERATION):
            self.__iteration(population)
        population.setIndividuals(population.selection(Constants.POPULATION_SIZE))
        self.__repository.setLastPopulation(population)

    def simulateSeed(self, crtSeed):
        random.seed(crtSeed)
        newPopulation = Population(Constants.POPULATION_SIZE, Constants.MAX_INDIVIDUAL_SIZE, (self.__drone.getX(), self.__drone.getY()), self.__mapSurface)
        self.__repository.addPopulation(newPopulation)

        bestIndividual = None
        lastAverageFitness = 0
        for generation in range(Constants.GENERATION_COUNT):
            self.__runGeneration(newPopulation)
            populationFitness = []
            for individual in newPopulation.getIndividuals():
                populationFitness.append(individual.getFitness())
            bestIndividual = newPopulation.selection(1)[0]
            lastAverageFitness = np.average(populationFitness)

        return lastAverageFitness, bestIndividual

    def runProgram(self):
        solutionAverages = []  # for each seed, average of the fitness for the final generation (= solution)
        bestIndividuals = []
        print("seed - final gen fitness avg - bestFitness")
        for seed in range(Constants.FIRST_SEED, Constants.LAST_SEED):
            finalGenerationAverage, bestIndividual = self.simulateSeed(seed)
            print("%02d - %.3f - %d" % (seed, finalGenerationAverage, bestIndividual.getFitness()))
            solutionAverages.append(finalGenerationAverage)
            bestIndividuals.append(bestIndividual)

        return solutionAverages, bestIndividuals

    def getMapSurface(self):
        return self.__map.getMapSurface()

    def getDroneXCoord(self):
        return self.__drone.getX()

    def getDroneYCoord(self):
        return self.__drone.getY()
