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

    ENERGY_LEVELS = 6  # starting from and including 0
    SENSOR_COUNT = 8
    INFINITY = 999999999
    EPOCH_COUNT = 1000
    ANT_COUNT = SENSOR_COUNT
    ALPHA = 1.9
    BETA = 0.9
    RHO = 0.05
    Q0 = 0.5
