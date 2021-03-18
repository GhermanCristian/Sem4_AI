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
    LEFT = 2
    DOWN = 3
    
    #define indexes variations 
    DIRECTIONS = [[-1, 0], [0, 1], [0, -1], [1, 0]]
    
    BOARD_FILL_PERCENTAGE = 0.2
    BOARD_WIDTH = 20
    BOARD_HEIGHT = 20
    TILE_SIZE = 20 # square tile
    
    SEPARATOR_SIZE = 10
    SCREEN_WIDTH = 2 * BOARD_WIDTH * TILE_SIZE + SEPARATOR_SIZE
    SCREEN_HEIGHT = BOARD_HEIGHT * TILE_SIZE
    
    EMPTY_POSITION = 0
    WALL = 1
    UNKNOWN_POSITION = -1
    
    TIME_INTERVAL_BETWEEN_MOVES = 400 # in miliseconds
    TIME_INTERVAL_FINAL_WAIT = 2000 # in miliseconds