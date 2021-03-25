from GUI import GUI
from repository import Repository
from service import Service
import numpy
import matplotlib.pyplot as plt
from constants import Constants
from datetime import datetime


def plotGraph(solutionAverages):
    plt.plot(solutionAverages)
    plt.savefig("solutionAverageFitness.png")


def logToFile(solutionAverages):
    logFile = open("results.txt", "a")
    logFile.write(str(datetime.now()) + "\n")
    logFile.write("Seeds = [%d, %d]; " % (Constants.FIRST_SEED, Constants.LAST_SEED))
    logFile.write("Pop.size = %d; Ind.size = %d; Generations = %d; " % (
        Constants.POPULATION_SIZE, Constants.MAX_INDIVIDUAL_SIZE, Constants.GENERATION_COUNT))
    logFile.write("Iterations/gen = %d; Mutation prob = %.2f; Crossover prob = %.2f\n" % (
        Constants.ITERATIONS_PER_GENERATION, Constants.MUTATION_PROBABILITY, Constants.CROSSOVER_PROBABILITY))
    logFile.write("Average of averages: %.3f\n" % numpy.average(solutionAverages))
    logFile.write("Stdev of averages: %.3f\n" % numpy.std(solutionAverages))
    logFile.write("\n")
    logFile.close()


def main():
    repository = Repository()
    service = Service(repository)
    solutionAverages = GUI(service).start()
    plotGraph(solutionAverages)
    logToFile(solutionAverages)


if __name__ == "__main__":
    main()
