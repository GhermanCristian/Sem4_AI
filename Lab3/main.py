from GUI import GUI
from individual import DFS, Individual, Population
from map import Map
from repository import Repository
from service import Service
import numpy
import matplotlib.pyplot as plt

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

    repo = Repository()
    service = Service(repo)
    service.addNewPopulation(50, 35, (5, 5))
    
    
    generation = 1
    generationAverageFitness = []
    generationFitnessStddev = []
    bestPath = None
    while generation <= 10:
        print ("generation = ", generation)
        service.runGeneration()
        population = service.getPopulations()[0]
        populationFitness = []
        for individual in population.getIndividuals():
            populationFitness.append(individual.getFitness())
        print ("best individual fitness: ", max(populationFitness))
        generationAverageFitness.append(numpy.average(populationFitness))
        generationFitnessStddev.append(numpy.std(populationFitness))
        bestPath = population.selection(1)[0]
        print ("avg fitness: ", numpy.average(populationFitness))
        print ()
        generation += 1
        
    plt.plot(generationAverageFitness)
    plt.savefig("avgFitness.png")
    plt.clf()
    plt.plot(generationFitnessStddev)
    plt.savefig("avgStddev.png")
    
    newGUI = GUI(service)
    newGUI.displayWithPath(bestPath.getChromosome())
    
if __name__ == "__main__":
    main()