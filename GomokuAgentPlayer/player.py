# Imports
import numpy as np
from copy import copy, deepcopy

from misc import legalMove, rowTest, diagTest, winningTest
from gomokuAgent import GomokuAgent

# Variables
opponent_id = 0
player_id = 0
priority_moves_queue = []

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


# Player Class
class Player(GomokuAgent):
    # Makes a legal player move depending on the opponents current tiles, and the 'best' move to make.
    def move(self, board):
        global opponent_id
        global player_id

        # Player and opponent ID assignment
        if player_id == 0:
            player_id = self.ID
        if opponent_id == 0:
            opponent_id = get_opponent_id(board)
            print("Opponent ID: " + str(opponent_id))

        best_move = None

        print ("Board score: {}".format(get_board_score(board, player_id)))

        best_moves = get_best_moves(board, player_id, 2)
        max_one, coord_one = minimax(board, best_moves[0], 3, player_id)
        max_two, coord_two = minimax(board, best_moves[1], 3, player_id)
        print("MAX ONE", max_one)
        print("COORD_ONE", coord_one)
        print("MAX TWO", max_two)
        print("COORD_TWO", coord_two)

        player_best_move = max(max_one,max_two)
        print (player_best_move)

        if (max_one == player_best_move):
            best_coord = coord_one
        else:
            best_coord = coord_two

        
       
        #opponent_best_move = get_best_move(board, opponent_id)

        #get_best_moves(board, player_id, 2)

        # Note: attack vs def. if second player to move, value block first
        #if (player_best_move[0] >= opponent_best_move[0]):
        #    best_coord = player_best_move[1]
        #else:
        #    best_coord = opponent_best_move[1]

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

    print ("Here are the tiles that belong to player_id={}:".format(player_id))
    print (given_id_tiles)
    print ()

    return given_id_tiles


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
    
    return row


# Get the star around 
def get_star(board, coords):
    star = []
    directions = [H, V, LD, RD]

    for direction in directions:
        row = get_row(board, coords, direction)
        star.append(row)

    return star


# Return score of tile
def get_tile_score(board, given_id, coords):
    copyboard = deepcopy(board)
    total_score = 0
    
    tile = get_tile(board, coords)
    value = tile[0]
    i, j = tile[1][0], tile[1][1]

    if (value == 0):
        copyboard[i][j] = given_id

    star = get_star(copyboard, coords)
    for x in range(len(star)):
        row_score = 0
    
        row = star[x]
        tile_score = 0
        consec = 0
        blocker = False
        for y in range(len(row)):
            tile = row[y]

            if (blocker == False):
                if (tile[0] == 0):
                    consec = 0
                elif (tile[0] == given_id):
                    consec += 1
                    tile_score = (int("1" * consec))
                    row_score += tile_score
                elif (tile[0] == opponent_id):
                    blocker = True
                    consec = 0

        total_score += row_score
        
    #print ("Score for {} for player_id={}: {}".format(
    #    coords, player_id, total_score))

    return [total_score, coords]


#
def get_board_score(board, given_id):
    board_score = 0
    other_id = given_id * -1
    
    board_coords = get_all_coords(board)
    given_id_score = 0
    other_id_score = 0
    
    for coords in board_coords:
        given_id_score = get_tile_score(board, given_id, coords)[0]
        other_id_score = get_tile_score(board, other_id, coords)[0] * -1
        tile_score = given_id_score + other_id_score
        board_score += tile_score

    print("Current player: {}, Opponent: {}".format(given_id, other_id))
    return board_score


#
def get_tile_scores(board, given_id):
    tiles = []
    board_coords = get_all_coords(board)

    for coords in board_coords:
        if (legalMove(board, coords)):
            tile = get_tile_score(board, given_id, coords)
            tiles.append(tile)
        
    tiles = sorted(tiles, key=lambda k: k[0], reverse=True)
    
    return tiles


#
def get_best_moves(board, given_id, amount):
    best_moves = []
    
    other_id = given_id * -1
    
    given_id_moves = get_tile_scores(board, given_id)
    other_id_moves = get_tile_scores(board, other_id)

    all_moves = given_id_moves + other_id_moves

    all_moves = sorted(all_moves, key=lambda k: k[0], reverse=True)

    i = 0 
    while (len(best_moves) < amount):
        best_move = all_moves[i]

        if (legalMove(board, best_move[1])):
            best_moves.append(best_move)

        i += 1

    print (best_moves)

    return (best_moves)

# Analyse player
def get_best_move(board, given_id):
    best_move = None

    if (check_centre(board) is not None):
        best_coords = check_centre(board)
        best_move = 11111, best_coords
        
    else:
        tiles = get_tile_scores(board, given_id)
        
        best_move_index = 0
        while True:
            best_move = tiles[best_move_index]
            tile_score = best_move[0]
            coords = best_move[1]

            if (legalMove(board, coords)):
                break

            best_move_index += 1

    return best_move


#
def minimax(board, depth, given_id):
    other_id = given_id * - 1
    
    if ((depth == 0) or (winningTest(given_id, board, 5)):
        return "winning condition"

    children = get_best_moves(board, given_id, 2)
    if (given_id == 1):
        max_eval= -99999
        
    
        

    




        
