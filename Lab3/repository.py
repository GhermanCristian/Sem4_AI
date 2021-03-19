from individual import Population
class Repository:
    def __init__(self):
        self.__populations = []
        
    def createPopulation(self, populationSize, individualMaxSize):
        self.__populations.append(Population(populationSize, individualMaxSize))