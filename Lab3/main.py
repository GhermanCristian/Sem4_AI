from GUI import GUI
from individual import DFS, Individual, Population
from map import Map
from repository import Repository
from service import Service
import numpy

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
    service.addNewPopulation(50, 30, (5, 5))
    newGUI = GUI(service)
    
    generation = 0
    while generation < 30:
        print ("generation = ", generation)
        service.runGeneration()
        population = service.getPopulations()[0]
        populationFitness = []
        for individual in population.getIndividuals():
            populationFitness.append(individual.getFitness())
        print ("best individual fitness: ", max(populationFitness))
        print ("avg fitness: ", numpy.average(populationFitness))
        print ()
        generation += 1
    
if __name__ == "__main__":
    main()