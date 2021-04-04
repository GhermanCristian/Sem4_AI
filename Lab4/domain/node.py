class Node:
    def __init__(self, xCoord, yCoord):
        self._xCoord = xCoord  # the coords are valid
        self._yCoord = yCoord

    def getX(self):
        return self._xCoord

    def getY(self):
        return self._yCoord
