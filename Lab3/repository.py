from individual import Population

class Repository:
    def __init__(self):
        self.__populations = []
        
    def addNewPopulation(self, populationSize, individualMaxSize, startingCoordinates, m):
        self.__populations.append(Population(populationSize, individualMaxSize, startingCoordinates, m))
        
    def getPopulations(self):
        return self.__populations
    
    def addExistingPopulation(self, newPopulation):
        self.__populations.append(newPopulation)