# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!
"""


class Solver:
    def __init__(self):
        """
        triangles are of the form (a, b, c), the x-coordinates of:
        a = left base; b = right base; c = apex
        """
        self.__angleTriangleSets = []
        self.__fillAngleTriangleSets()
        self.__angularSpeedTriangleSets = []
        self.__fillAngularSpeedTriangleSets()

    def __fillAngleTriangleSets(self):
        self.__angleTriangleSets.append((-40, -25, -40))  # NVB
        self.__angleTriangleSets.append((-40, -10, -25))  # NB
        self.__angleTriangleSets.append((-20, 0, -10))  # N
        self.__angleTriangleSets.append((-5, 5, 0))  # ZO
        self.__angleTriangleSets.append((0, 20, 10))  # P
        self.__angleTriangleSets.append((10, 40, 25))  # PB
        self.__angleTriangleSets.append((25, 40, 40))  # PVB

    def __fillAngularSpeedTriangleSets(self):
        self.__angularSpeedTriangleSets.append((-8, -3, -8))  # NB
        self.__angularSpeedTriangleSets.append((-6, 0, -3))  # N
        self.__angularSpeedTriangleSets.append((-1, 1, 0))  # ZO
        self.__angularSpeedTriangleSets.append((0, 6, 3))  # P
        self.__angularSpeedTriangleSets.append((3, 8, 8))  # PB

    def solve(self, t, w):
        """
        Parameters
        ----------
        t : TYPE: float
            DESCRIPTION: the angle theta
        w : TYPE: float
            DESCRIPTION: the angular speed omega

        Returns
        -------
        F : TYPE: float
            DESCRIPTION: the force that must be applied to the cart
        or

        None :if we have a division by zero

        """
        return None
