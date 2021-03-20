import random
from constants import Constants
import numpy as np

class Gene:
    def __init__(self, directionCode):
        self.__directionCode = directionCode
        
    def setDirectionCode(self, newDirectionCode):
        self.__directionCode = newDirectionCode
        
    def getDirectionCode(self):
        return self.__directionCode
              
class DFS:
    def __init__(self, m, requiredLength, initialX, initialY):
        self.__visitedPositions = []
        self.__visitedPositions.append((initialX, initialY))
        self.__predecessor = {}
        self.__predecessor[(initialX, initialY)] = None
        self.__map = m
        self.__requiredLength = requiredLength
        self.__alreadyFound = False
        self.__initialX, self.__initialY = initialX, initialY
        self.__finalX, self.__finalY = initialX, initialY
        self.__newDirections = random.sample(Constants.DIRECTIONS, 4) #otherwise everyone would have the same path every time
        
    def __DFS(self, crtX, crtY, crtLength):
        if self.__alreadyFound:
            return
        
        if self.__requiredLength == crtLength:
            if random.random() < 0.25: # we don't want to always select the first valid path, to reduce repetition
                self.__alreadyFound = True
                self.__finalX, self.__finalY = crtX, crtY
            return
        
        for direction in self.__newDirections:
            newX = crtX + direction[0]
            newY = crtY + direction[1]
            if (newX, newY) not in self.__visitedPositions and 0 <= newX < Constants.MAP_HEIGHT and 0 <= newY < Constants.MAP_WIDTH\
            and self.__map[newX][newY] == Constants.EMPTY_POSITION:
                self.__predecessor[(newX, newY)] = (crtX, crtY)
                self.__visitedPositions.append((newX, newY))
                self.__DFS(newX, newY, crtLength + 1)
                
    def __retracePath(self):
        pathAsDirectionCodes = []
        directionCodeDictionary = {(-1, 0) : 0, (0, 1) : 1, (1, 0) : 2, (0, -1) : 3}
        newX, newY = self.__finalX, self.__finalY
        while self.__predecessor[(newX, newY)] is not None:
            direction = (newX - self.__predecessor[(newX, newY)][0], newY - self.__predecessor[(newX, newY)][1])
            pathAsDirectionCodes.append(directionCodeDictionary[direction])
            newX, newY = self.__predecessor[(newX, newY)]
        pathAsDirectionCodes.reverse()
        return pathAsDirectionCodes        
                
    def start(self):
        self.__DFS(self.__initialX, self.__initialY, 1)
        return self.__retracePath()

class PathFixer:
    def __init__(self, startingPoint, directionCodes, m):
        self.__startingPoint = startingPoint
        self.__directionCodes = directionCodes
        self.__map = m
        self.__visitedPositions = []
        self.__visitedPositions.append(startingPoint)
    
    def __validPosition(self, newX, newY):
        return 0 <= newX < Constants.MAP_HEIGHT and 0 <= newY < Constants.MAP_WIDTH and \
            self.__map[newX][newY] == Constants.EMPTY_POSITION and (newX, newY) not in self.__visitedPositions

    def fixPath(self):
        crtX, crtY = self.__startingPoint
        validPathDirectionCodes = []
        for directionCode in self.__directionCodes:
            direction = Constants.DIRECTIONS[directionCode]
            
            if self.__validPosition(crtX + direction[0], crtY + direction[1]):
                crtX += direction[0]
                crtY += direction[1]
                self.__visitedPositions.append((crtX, crtY))
                validPathDirectionCodes.append(directionCode)
        
        return validPathDirectionCodes

class Individual:
    def __init__(self, maxSize, startingCoordinates, m):
        self.__maxSize = maxSize # this will be the number of genes = path length - 1
        self.__startingCoordinates = startingCoordinates
        self.__map = m # this is already a map surface
        self.__chromosome = []
        self.__fitness = None   
       
    def generateChromosome(self):
        self.__chromosome = DFS(self.__map, self.__maxSize + 1, self.__startingCoordinates[0], self.__startingCoordinates[1]).start()
    
    def setChromosome(self, newChromosome):
        self.__chromosome = newChromosome
    
    def getChromosome(self):
        return self.__chromosome
    
    def getFitness(self):
        return self.__fitness # it might be none, if we haven't computed the fitness for this individual until now
    
    def __checkEmptyAndUpdateAccessibleCount(self, crtCoords, temporaryMatrix):
        if temporaryMatrix[crtCoords[0]][crtCoords[1]] == Constants.ACCESSIBLE_POSITION:
            return 0
        temporaryMatrix[crtCoords[0]][crtCoords[1]] = Constants.ACCESSIBLE_POSITION
        return 1
    
    def __markAndCountNewAccessible(self, temporaryMatrix, crtCoords):
        newAccessible = 0
        
        newX = crtCoords[0] - 1 # UP
        while newX >= 0 and temporaryMatrix[newX][crtCoords[1]] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((newX, crtCoords[1]), temporaryMatrix)
            newX -= 1
            
        newY = crtCoords[1] + 1 # RIGHT
        while newY < Constants.MAP_WIDTH and temporaryMatrix[crtCoords[0]][newY] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((crtCoords[0], newY), temporaryMatrix)
            newY += 1
            
        newX = crtCoords[0] + 1 # DOWN
        while newX < Constants.MAP_HEIGHT and temporaryMatrix[newX][crtCoords[1]] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((newX, crtCoords[1]), temporaryMatrix)
            newX += 1
            
        newY = crtCoords[1] - 1 # LEFT
        while newY >= 0 and temporaryMatrix[crtCoords[0]][newY] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((crtCoords[0], newY), temporaryMatrix)
            newY -= 1
        
        return newAccessible
        
    def computeFitness(self):
        temporaryMatrix = self.__map.copy()
        
        crtCoords = self.__startingCoordinates # each gene is the code for a direction (UP = 0, DOWN = 2, LEFT = 1, RIGHT = 3)
        self.__fitness = self.__markAndCountNewAccessible(temporaryMatrix, crtCoords)
        
        # we also assume that the path is correct in this point; it is corrected when mutating or doing a crossover
        for gene in self.__chromosome:
            direction = Constants.DIRECTIONS[gene]
            crtCoords = (crtCoords[0] + direction[0], crtCoords[1] + direction[1])
            self.__fitness += self.__markAndCountNewAccessible(temporaryMatrix, crtCoords)
    
    def __mutate(self):
        # perform a mutation with respect to the representation
        lastChromosomeIndex = len(self.__chromosome) - 1
        if random.random() < 0.15: 
            firstGene, lastGene = 0, lastChromosomeIndex // 2 # mutate something in the first half of the chromosome
        else:
            firstGene, lastGene = lastChromosomeIndex // 2 + 1, lastChromosomeIndex # mutate sth in the second half of the chromosome

        affectedGene = random.randint(firstGene, lastGene)
        self.__chromosome[affectedGene] = (self.__chromosome[affectedGene] + random.randint(1, 3)) % 4
        
        self.__chromosome = PathFixer(self.__startingCoordinates, self.__chromosome, self.__map).fixPath()
    
    def attemptMutation(self, mutateProbability):
        if random.random() < mutateProbability:
            self.__mutate()
    
    def __crossover(self, otherParent):
        offspring = Individual(self.__maxSize, self.__startingCoordinates, self.__map)
        firstChromosome = self.__chromosome
        firstChromosomeLength = len(firstChromosome)
        secondChromosome = otherParent.getChromosome()
        secondChromosomeLength = len(secondChromosome)
        
        if firstChromosomeLength <= 2 or secondChromosomeLength <= 2:
            return None
        
        crossoverPoint = random.randint(1, min(firstChromosomeLength, secondChromosomeLength) - 2)
        
        newChromosome = firstChromosome[:crossoverPoint]
        newChromosome.extend(secondChromosome[crossoverPoint:])
        offspring.setChromosome(PathFixer(self.__startingCoordinates, newChromosome, self.__map).fixPath())
        
        if len(offspring.getChromosome()) > self.__maxSize:
            print ("we have a problem")
        return offspring
    
    def attemptCrossover(self, otherParent, crossoverProbability):
        if random.random() < crossoverProbability:
            return self.__crossover(otherParent)
        
        return None
    
class Population():
    def __init__(self, populationSize, individualMaxSize, startingCoordinates, m):
        self.__populationSize = populationSize
        self.__map = m # already a map surface
        self.__individuals = []
        for i in range(populationSize):
            newIndividual = Individual(individualMaxSize, startingCoordinates, self.__map)
            newIndividual.generateChromosome()
            newIndividual.computeFitness()
            self.__individuals.append(newIndividual)
        
    def evaluate(self):
        for x in self.__individuals:
            x.computeFitness()
            
    def selection(self, k):
        return sorted(self.__individuals, key = lambda elem : elem.getFitness(), reverse=True)[:k]
    
    def getIndividuals(self):
        return self.__individuals
    
    def addIndividual(self, newIndividual):
        self.__individuals.append(newIndividual)
        
    def removeIndividualByIndex(self, index):
        return self.__individuals.pop(index)

    def setIndividuals(self, newIndividuals):
        self.__individuals.clear()
        self.__individuals.extend(newIndividuals)