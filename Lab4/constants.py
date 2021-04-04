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
    DRONE_BATTERY = 100
    SENSOR_COUNT = 8
    INFINITY = 999999999
    EPOCH_COUNT = 100
    NODES_PER_SENSOR = 2 + ENERGY_LEVELS  # each sensor has an entry and exit node + energy level
    NODE_COUNT = SENSOR_COUNT * NODES_PER_SENSOR
    MOVE_COUNT = 3 * SENSOR_COUNT  # to get from one sensor to another: choose energy level, go to exit, go to next node (3 moves)
    ANT_COUNT = NODE_COUNT * 32
    ALPHA = 1.9
    BETA = 0.9
    RHO = 0.03
    Q0 = 0.5
