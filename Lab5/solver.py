# -*- coding: utf-8 -*-

class Solver:
    MINIMUM_ANGLE = -40  # degrees
    MAXIMUM_ANGLE = 40
    MINIMUM_ANGULAR_SPEED = -8
    MAXIMUM_ANGULAR_SPEED = 8

    def __init__(self):
        """
        triangles are of the form (a, b, c), the x-coordinates of:
        a = left base; b = right base; c = apex
        """
        self.__angleTriangleSets = []
        self.__fillAngleTriangleSets()
        self.__angularSpeedTriangleSets = []
        self.__fillAngularSpeedTriangleSets()

    def __computeMembershipDegree(self, x, triangleSet):
        # triangleSet: 0 -> a; 1 -> b; 2 -> c
        if x <= triangleSet[0] or x >= triangleSet[1]:
            return 0
        if x <= triangleSet[2]:
            if triangleSet[0] == triangleSet[2]:
                return 1
            return (x - triangleSet[0]) / (triangleSet[2] - triangleSet[0])
        if triangleSet[1] == triangleSet[2]:
            return 1
        return (triangleSet[1] - x) / (triangleSet[1] - triangleSet[2])

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

    def __computeAngleMembershipDegrees(self, angle):
        if angle < Solver.MINIMUM_ANGLE:
            angle = Solver.MINIMUM_ANGLE
        if angle > Solver.MAXIMUM_ANGLE:
            angle = Solver.MAXIMUM_ANGLE
        degrees = []
        for triangleSet in self.__angleTriangleSets:
            degrees.append(self.__computeMembershipDegree(angle, triangleSet))
        return degrees

    def __computeAngularSpeedMembershipDegrees(self, angularSpeed):
        if angularSpeed < Solver.MINIMUM_ANGULAR_SPEED:
            angularSpeed = Solver.MINIMUM_ANGULAR_SPEED
        if angularSpeed > Solver.MAXIMUM_ANGULAR_SPEED:
            angularSpeed = Solver.MAXIMUM_ANGULAR_SPEED
        degrees = []
        for triangleSet in self.__angularSpeedTriangleSets:
            degrees.append(self.__computeMembershipDegree(angularSpeed, triangleSet))
        return degrees

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
