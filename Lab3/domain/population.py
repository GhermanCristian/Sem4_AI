from domain.individual import Individual


class Population:
    def __init__(self, populationSize, individualMaxSize, startingCoordinates, m):
        self.__populationSize = populationSize
        self.__map = m  # already a map surface
        self.__individuals = []
        for i in range(populationSize):
            newIndividual = Individual(individualMaxSize, startingCoordinates, self.__map)
            newIndividual.generateChromosome()
            self.__individuals.append(newIndividual)
        self.evaluate()

    def evaluate(self):
        for x in self.__individuals:
            x.computeFitness()

    def selection(self, k):
        totalFitnessSum = 0
        for individual in self.__individuals:
            totalFitnessSum += individual.getFitness()
        return sorted(self.__individuals, key=lambda elem: elem.getFitness(), reverse=True)[:k]

    def getIndividuals(self):
        return self.__individuals

    def addIndividual(self, newIndividual):
        self.__individuals.append(newIndividual)

    def removeIndividualByIndex(self, index):
        return self.__individuals.pop(index)

    def setIndividuals(self, newIndividuals):
        self.__individuals.clear()
        self.__individuals.extend(newIndividuals)
