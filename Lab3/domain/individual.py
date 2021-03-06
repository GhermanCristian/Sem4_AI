import random
from constants import Constants
from domain.DFS import DFS
from domain.pathFixer import PathFixer


class Individual:
    def __init__(self, maxSize, startingCoordinates, m):
        self.__maxSize = maxSize  # this will be the number of genes = path length - 1
        self.__startingCoordinates = startingCoordinates
        self.__map = m  # this is already a map surface
        self.__chromosome = []
        self.__fitness = None

    def generateChromosome(self):
        self.__chromosome = DFS(self.__map, self.__maxSize + 1, self.__startingCoordinates[0],
                                self.__startingCoordinates[1]).start()

    def setChromosome(self, newChromosome):
        self.__chromosome = newChromosome

    def getChromosome(self):
        return self.__chromosome

    def getFitness(self):
        return self.__fitness  # it might be none, if we haven't computed the fitness for this individual yet

    def __checkEmptyAndUpdateAccessibleCount(self, crtCoords, temporaryMatrix):
        if temporaryMatrix[crtCoords[0]][crtCoords[1]] == Constants.ACCESSIBLE_POSITION:
            return 0
        temporaryMatrix[crtCoords[0]][crtCoords[1]] = Constants.ACCESSIBLE_POSITION
        return 1

    def __markAndCountNewAccessible(self, temporaryMatrix, crtCoords):
        newAccessible = 0

        newX = crtCoords[0] - 1  # UP
        while newX >= 0 and temporaryMatrix[newX][crtCoords[1]] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((newX, crtCoords[1]), temporaryMatrix)
            newX -= 1

        newY = crtCoords[1] + 1  # RIGHT
        while newY < Constants.MAP_WIDTH and temporaryMatrix[crtCoords[0]][newY] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((crtCoords[0], newY), temporaryMatrix)
            newY += 1

        newX = crtCoords[0] + 1  # DOWN
        while newX < Constants.MAP_HEIGHT and temporaryMatrix[newX][crtCoords[1]] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((newX, crtCoords[1]), temporaryMatrix)
            newX += 1

        newY = crtCoords[1] - 1  # LEFT
        while newY >= 0 and temporaryMatrix[crtCoords[0]][newY] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((crtCoords[0], newY), temporaryMatrix)
            newY -= 1

        return newAccessible

    def computeFitness(self):
        temporaryMatrix = self.__map.copy()
        crtCoords = self.__startingCoordinates
        self.__fitness = self.__markAndCountNewAccessible(temporaryMatrix, crtCoords)

        # we also assume that the path is correct in this point; it is fixed when mutating or doing a crossover
        for gene in self.__chromosome:
            direction = Constants.DIRECTIONS[gene]
            crtCoords = (crtCoords[0] + direction[0], crtCoords[1] + direction[1])
            self.__fitness += self.__markAndCountNewAccessible(temporaryMatrix, crtCoords)

    def __mutate(self):
        # perform a mutation with respect to the representation
        lastChromosomeIndex = len(self.__chromosome) - 1
        if lastChromosomeIndex < 0:
            return
        if lastChromosomeIndex <= 3:
            affectedGene = random.randint(0, lastChromosomeIndex)
        else:
            if random.random() < 0.15:
                # mutate something in the first half of the chromosome
                firstGene, lastGene = 0, lastChromosomeIndex // 2
            else:
                # mutate sth in the second half of the chromosome
                firstGene, lastGene = lastChromosomeIndex // 2 + 1, lastChromosomeIndex

            affectedGene = random.randint(firstGene, lastGene)

        self.__chromosome[affectedGene] = (self.__chromosome[affectedGene] + random.randint(1, 3)) % 4
        self.__chromosome = PathFixer(self.__startingCoordinates, self.__chromosome, self.__map).fixPath()

    def attemptMutation(self, mutateProbability):
        if random.random() < mutateProbability:
            self.__mutate()

    def __crossover(self, otherParent):
        offspring = Individual(self.__maxSize, self.__startingCoordinates, self.__map)
        firstChromosome = self.__chromosome
        secondChromosome = otherParent.getChromosome()

        newChromosome = firstChromosome.copy()
        newChromosome.extend(secondChromosome)
        extraLength = len(newChromosome) - self.__maxSize
        if extraLength > 0:
            # remove a section of length = extraLength
            firstRemovedIndex = random.randint(0, len(newChromosome) - extraLength - 1)
            lastRemovedIndex = firstRemovedIndex + extraLength
            del newChromosome[firstRemovedIndex : lastRemovedIndex + 1]  # +1 because python slices don't include the last elem

        offspring.setChromosome(PathFixer(self.__startingCoordinates, newChromosome, self.__map).fixPath())
        return offspring

    def attemptCrossover(self, otherParent, crossoverProbability):
        if random.random() < crossoverProbability:
            return self.__crossover(otherParent)

        return None
