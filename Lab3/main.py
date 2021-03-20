from GUI import GUI
from repository import Repository
from service import Service
import numpy
import matplotlib.pyplot as plt
from constants import Constants
import random

def simulateSeed():
    repo = Repository()
    service = Service(repo)
    service.addNewPopulation(Constants.POPULATION_SIZE, Constants.MAX_INDIVIDUAL_SIZE, (5, 5))
    
    bestIndividualFitness = 0
    lastAverageFitness = 0
    for generation in range(Constants.GENERATION_COUNT):
        service.runGeneration()
        population = service.getPopulations()[0]
        populationFitness = []
        for individual in population.getIndividuals():
            populationFitness.append(individual.getFitness())
        bestIndividualFitness = max(bestIndividualFitness, max(populationFitness))
        lastAverageFitness = numpy.average(populationFitness)
        
    return lastAverageFitness, bestIndividualFitness

def logToFile(solutionAverages):
    logFile = open("results.txt", "a")
    logFile.write("Seeds = [%d, %d]; " % (Constants.FIRST_SEED, Constants.LAST_SEED))
    logFile.write("Pop.size = %d; Ind.size = %d; Generations = %d; " % (Constants.POPULATION_SIZE, Constants.MAX_INDIVIDUAL_SIZE, Constants.GENERATION_COUNT))
    logFile.write("Iterations/gen = %d; Mutation prob = %.2f; Crossover prob = %.2f\n" % (Constants.ITERATIONS_PER_GENERATION, Constants.MUTATION_PROBABILITY, Constants.CROSSOVER_PROBABILITY))
    logFile.write("Average of averages: %.3f\n" % numpy.average(solutionAverages))
    logFile.write("Stdev of averages: %.3f\n" % numpy.std(solutionAverages))
    logFile.write("\n")
    logFile.close()

def main():
    # create a menu
    #   1. map options:
    #         a. create random map
    #         b. load a map
    #         c. save a map
    #         d visualise map
    #   2. EA options:
    #         a. parameters setup
    #         b. run the solver
    #         c. visualise the statistics
    #         d. view the drone moving on a path
    #              function gui.movingDrone(currentMap, path, speed, markseen)
    #              ATENTION! the function doesn't check if the path passes trough walls

    solutionAverages = [] # for each seed, average of the fitness for the final generation (= solution)
    print ("seed - final gen fitness avg - bestFitness")
    for i in range(Constants.FIRST_SEED, Constants.LAST_SEED):
        random.seed(i)
        finalGenerationAverage, bestFitness = simulateSeed()
        print ("%0d - %.3f - %d" % (i, finalGenerationAverage, bestFitness))
        solutionAverages.append(finalGenerationAverage)
    
    logToFile(solutionAverages)
    plt.plot(solutionAverages)
    plt.savefig("solutionAverageFitness.png")
    
if __name__ == "__main__":
    main()