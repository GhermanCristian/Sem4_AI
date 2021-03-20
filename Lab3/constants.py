class Constants:
    #Creating some colors
    BLUE  = (0, 0, 255)
    GRAYBLUE = (50,120,120)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    #define directions
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    #define indexes variations 
    DIRECTIONS = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    
    MAP_HEIGHT = 20 # in no. of tiles
    MAP_WIDTH = 20
    
    EMPTY_POSITION = 0
    WALL_POSITION = 1
    ACCESSIBLE_POSITION = 2
    
    TIME_BETWEEN_MOVES = 50 # in miliseconds
    POPULATION_SIZE = 50
    MAX_INDIVIDUAL_SIZE = 35
    ITERATIONS_PER_GENERATION = 1000
    MUTATION_PROBABILITY = 0.05
    CROSSOVER_PROBABILITY = 0.8
    GENERATION_COUNT = 13
    
    FIRST_SEED = 50
    LAST_SEED = 100