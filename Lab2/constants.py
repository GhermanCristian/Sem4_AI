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
    DOWN = 2
    LEFT = 1
    RIGHT = 3
    
    #define indexes variations 
    DIRECTIONS = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    
    MAP_HEIGHT = 20 # in no. of tiles
    MAP_WIDTH = 20
    
    TIME_BETWEEN_MOVES = 150 # in miliseconds
    
    A_STAR_NAME = "A*"
    GREEDY_NAME = "Greedy"
    NORMAL_HILL_CLIMBING_NAME = "NormalHillClimbing"
    STEEPEST_HILL_CLIMBING_NAME = "SteepestHillClimbing"
    DFS_NAME = "DFS"