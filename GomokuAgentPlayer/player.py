# Imports
import math
import numpy as np
from copy import copy, deepcopy

from misc import legalMove, rowTest, diagTest, winningTest
from gomokuAgent import GomokuAgent

# Variables
opponent_id = 0
player_id = 0
priority_moves_queue = []
move_count = 0

# Constants
N = "NORTH"
S = "SOUTH"
W = "WEST"
E = "EAST"
NE = "NORTH-EAST"
NW = "NORTH-WEST"
SE = "SOUTH-EAST"
SW = "SOUTH-WEST"

H = "HORIZONTAL"
V = "VERTICAL"
LD = "LEFT-DIAGONAL"
RD = "RIGHT-DIAGONAL"

EMPTY = 0


# Player Class
class Player(GomokuAgent):
    # Makes a legal player move depending on the opponents current tiles, and the 'best' move to make.
    def move(self, board):
        global opponent_id
        global player_id
        global move_count

        # Player and opponent ID assignment
        if player_id == 0:
            player_id = self.ID
        if opponent_id == 0:
            opponent_id = get_opponent_id(board)
            print("Opponent ID: " + str(opponent_id))

        move_count += 1
        print ("Move #{}".format(move_count))

        best_move = None

        #print ("Board score: {}".format(get_board_score(board)))

        #best_moves = get_best_moves(board, player_id, 2)

        player_best_move = get_best_move(board, player_id)

        #get_best_moves(board, player_id, 2)

        # Note: attack vs def. if second player to move, value block first
        #if (player_best_move[0] >= opponent_best_move[0]):
        #    best_coord = player_best_move[1]
        #else:
        #    best_coord = opponent_best_move[1]

        best_coord = player_best_move[1]

        print("Placing tile at: " + str(best_coord))
        
        return best_coord


# Makes a random legal move.
def move_randomly(self, board):
    while True:
        move_loc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
        print("Move loc:", move_loc)
        if legalMove(board, move_loc):
            return move_loc


# Returns centre tile coords if empty and None otherwise
def check_centre(board):
    size = len(board)
    mid = size // 2
    mid_tile = (mid, mid)
    if legalMove(board, mid_tile):
        return mid_tile


# Returns the opponents ID. Only called once per game.
def get_opponent_id(board):
    for row in board:
        for tile in row:
            if (tile != player_id and tile != 0):
                return tile

    return (player_id * -1)


# Returns all the coordinates from the board
def get_all_coords(board):
    coords = []
    for i in range(len(board)):
        for j in range(len(board)):
            tile = get_tile(board, (i, j))
            coords.append(tile[1])
    return coords


# Return tile value and coordinates of a given player
def get_player_tiles(board, given_id):
    given_id_tiles = []
    n = len(board)
    
    for i in range(n):
        for j in range(n):
            if (board[i][j] == given_id):
                coords = (i, j)
                given_id_tile = get_tile(board, coords)
                given_id_tiles.append(player_tile)

    print ("Here are the tiles that belong to player_id={}:".format(given_id))
    print (given_id_tiles)
    print ()

    return given_id_tiles


# Returns all the coordinates from the board that are empty
def get_empty_coords(board):
    coords = []
    for i in range(len(board)):
        for j in range(len(board)):
            tile = get_tile(board, (i, j))
            if (tile[0] == EMPTY):
                coords.append(tile[1])
    return coords


# Get value and coordinates of a tile
def get_tile(board, coords):
    size = len(board)
    i, j = coords[0], coords[1]
    # print ("The value at {} is {}.\n".format(coords, value))
    if (0 <= i < size and 0 <= j < size):
        value = board[i][j]
        tile = [value, coords]
        return tile
    else:
        return [None, None]


# Return tile in specified direction
def look(board, coords, direction):
    tile = [None, None]
    
    if (coords is not None):
        i, j = coords[0], coords[1]

        # North
        if (direction == N):
            tile = get_tile(board, (i - 1, j))
        # North-east
        elif (direction == NE):
            tile = get_tile(board, (i - 1, j + 1))
        # East
        elif (direction == E):
            tile = get_tile(board, (i, j + 1))
        # South-east
        elif (direction == SE):
            tile = get_tile(board, (i + 1, j + 1))
        # South
        elif (direction == S):
            tile = get_tile(board, (i + 1, j))
        # South-west
        elif (direction == SW):
            tile = get_tile(board, (i + 1, j - 1))
        # West
        elif (direction == W):
            tile = get_tile(board, (i, j - 1))
        # North-west
        elif (direction == NW):
            tile = get_tile(board, (i - 1, j - 1))

        # Info
        #if (tile[1] is not None):
        #    print ("The tile {} of {} is {}.".format(
        #        direction.lower(), coords, tile))
        #else:
        #    print ("There is no tile {} of {}.".format(
        #        direction.lower(), coords))

    return tile


# Check 9-long row of tiles
def get_row(board, coords, direction):
    row = []
    directions = []
    
    tile = get_tile(board, coords)
    value = tile[0]

    # Horizontal
    if (direction == H):
        directions.append(W)
        directions.append(E)
    # Vertical
    elif (direction == V):
        directions.append(N)
        directions.append(S)
    # Left-diagonal
    elif (direction == LD):
        directions.append(NW)
        directions.append(SE)
    # Right-diagonal
    elif (direction == RD):
        directions.append(NE)
        directions.append(SW)
        
    left_start, right_start = (look(board, coords, directions[0]),
                     look(board, coords, directions[1]))
    
    left_m1, right_m1 = (look(board, left_start[1], directions[0]),
                     look(board, right_start[1], directions[1]))
    
    left_m2, right_m2 = (look(board, left_m1[1], directions[0]),
                     look(board, right_m1[1], directions[1]))
    
    left_end, right_end = (look(board, left_m2[1], directions[0]),
                     look(board, right_m2[1], directions[1]))

    row = [left_end, left_m2, left_m1, left_start,
           tile,
           right_start, right_m1, right_m2, right_end]

    final_row = []
    for i in range(len(row)):
        if row[i] != [None, None]:
            final_row.append(row[i])
    
    return final_row


# Get the star around 
def get_star(board, coords):
    star = []
    directions = [H, V, LD, RD]

    for direction in directions:
        row = get_row(board, coords, direction)
        star.append(row)

    return star


#
def row_possible(row, given_id):
    max_row_size = 0
    count = 0

    for tile in row:
        value = tile[0]
        if value == EMPTY or value == given_id:
            count += 1
        else:
            if count > max_row_size:
                max_row_size = count
            count = 0

    return max_row_size >= 5


#
def get_row_score(row, given_id):
    other_id = given_id * -1

    row_score = 0
    consec = 0
    for tile in row:
        if tile[0] == given_id:
            consec += 1
        if tile[0] != given_id and consec > 0:
            row_score += int(math.pow(10, consec)) - 1
            consec = 0
        elif tile[0] == EMPTY:
            row_score += 1

    #print ("{} to {}; Score: {}".format(row[0], row[-1], row_score))

    return row_score


# TODO: Change so it predicted new value of tile
# Return score of tile
def get_tile_score(board, given_id, coords):
    other_id = given_id * -1
    copyboard = deepcopy(board)
    total_score = 0

    tile = get_tile(board, coords)
    value = tile[0]
    i, j = tile[1]

    if (value == EMPTY):
        copyboard[i][j] = given_id
    else:
        return [0, coords]

    star = get_star(copyboard, coords)
    for x in range(len(star)):
        row = star[x]

        row_score = get_row_score(row, given_id)
        
        total_score += row_score
        


    #print ("Score for {} for player_id={}: {}".format(
    #    coords, player_id, total_score))

    #print ("{}: Score: {}".format(coords, total_score))

    return [total_score, coords]


#
def get_tile_scores(board, given_id):
    tiles = []
    empty_coords = get_empty_coords(board)

    for coords in empty_coords:
        tile = get_tile_score(board, given_id, coords)
        tiles.append(tile)

    tiles = sorted(tiles, key=lambda k: k[0], reverse=True)
    
    return tiles


# Analyse player
def get_best_move(board, given_id):
    other_id = given_id * -1
    best_move = None

    given_tile_scores = get_tile_scores(board, given_id)
    other_tile_scores = get_tile_scores(board, other_id)

    

    # tiles = get_tile_scores(board, given_id)

    best_given_move = given_tile_scores[0]
    best_other_move = other_tile_scores[0]

    print ("Best move for {}: {}\nBest move for {}: {}".format(
        given_id,
        best_given_move,
        other_id,
        best_other_move))

    if best_given_move > best_other_move:
        best_move = best_given_move
    else:
        best_move = best_other_move
    
    return best_move













