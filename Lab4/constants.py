class Constants:
    # Creating some colors
    BLUE = (0, 0, 255)
    GRAYBLUE = (50, 120, 120)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PINK = (255, 20, 147)

    # define directions
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    # define indexes variations
    DIRECTIONS = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    MAP_HEIGHT = 20  # in no. of tiles
    MAP_WIDTH = 20

    EMPTY_POSITION = 0
    WALL_POSITION = 1
    ACCESSIBLE_POSITION = 2
    SENSOR_POSITION = 3

    TIME_BETWEEN_MOVES = 50  # in milliseconds
    INFINITY = 999999999

    SENSOR_COUNT = 8
