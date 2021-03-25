from domain.population import Population


class Repository:
    def __init__(self):
        self.__populations = []
        
    def addPopulation(self, population):
        self.__populations.append(population)

    def setLastPopulation(self, population):
        self.__populations[-1] = population

    def getPopulations(self):
        return self.__populations
        
    def removeAllPopulations(self):
        self.__populations.clear()
