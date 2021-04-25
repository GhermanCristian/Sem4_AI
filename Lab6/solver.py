class Solver:
    def __init__(self):
        self.__pointList = []  # a point is of the form (label, val1, val2)

    def __parseLineAndAddToList(self, line):
        splitData = line.split(",")
        self.__pointList.append((splitData[0], float(splitData[1]), float(splitData[2])))

    def __parseDataset(self):
        fileDesc = open("dataset.csv", "r")
        fileDesc.readline()  # skip the first line (header)
        for line in fileDesc:
            self.__parseLineAndAddToList(line[:-1])  # remove the trailing '\n'

    def solve(self):
        self.__parseDataset()
        for point in self.__pointList:
            print(point)

