# Imports
import numpy as np
from copy import deepcopy
import math
from misc import legalMove, winningTest
from gomokuAgent import GomokuAgent

# Variables
opponent_id = 0
player_id = 0
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
DIRECTIONS = [N, NE, E, SE, S, SW, W, NW]

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

        player_id = self.ID
        opponent_id = get_opponent_id(board)

        move_count += 1
        print("Move #{}".format(move_count))

        player_best_move = None

        # check if first turn and place tile in center
        # get rows of four
        # get rows of three
        # if none of the above run min max
        try:
            print("PLAYER TO MOVE: {}".format(self.ID))
            opponent_contains_inf = False
            opponent_best_moves = get_best_moves(board, opponent_id, 4)
            for move in opponent_best_moves:
                if move[0] == math.inf and legalMove(board, move[1]):
                    player_best_move = move[1]
                    opponent_contains_inf = True
            if not opponent_contains_inf:
                player_best_moves = get_best_moves(board, player_id, 4)
                for move in player_best_moves:
                    if move[0] == math.inf and legalMove(board, move[1]):
                        player_best_move = move[1]
            if player_best_move is None:
                player_best_move = minimax(board, 4, self.ID)[1]
        except IndexError:
            coords = get_empty_coords(board)
            player_best_move = coords[0]

        print("Player {} best move: {}".format(self.ID, player_best_move))
        return player_best_move

        # opponent_best_move = get_best_move(board, opponent_id)

        # get_best_moves(board, player_id, 2)

        # Note: attack vs def. if second player to move, value block first
        # if (player_best_move[0] >= opponent_best_move[0]):
        #    best_coord = player_best_move[1]
        # else:
        #    best_coord = opponent_best_move[1]

        # print("Placing tile at: " + str(best_coord))
        
        # return best_coord


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
            if tile != player_id and tile != 0:
                return tile

    return player_id * -1


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
            if board[i][j] == given_id:
                coords = (i, j)
                given_id_tile = get_tile(board, coords)
                given_id_tiles.append(given_id_tile)

    print("Here are the tiles that belong to player_id={}:".format(given_id))
    print(given_id_tiles)
    print()

    return given_id_tiles


# Returns all the coordinates from the board that are empty
def get_empty_coords(board):
    coords = []
    for i in range(len(board)):
        for j in range(len(board)):
            tile = get_tile(board, (i, j))
            if tile[0] == EMPTY:
                coords.append(tile[1])
    return coords


# Get value and coordinates of a tile
def get_tile(board, coords):
    size = len(board)
    i, j = coords[0], coords[1]
    # print ("The value at {} is {}.\n".format(coords, value))
    if 0 <= i < size and 0 <= j < size:
        value = board[i][j]
        tile = [value, coords]
        return tile
    else:
        return [None, None]


# Return tile in specified direction
def look(board, coords, direction):
    tile = [None, None]
    
    if coords is not None:
        i, j = coords[0], coords[1]

        # North
        if direction == N:
            tile = get_tile(board, (i - 1, j))
        # North-east
        elif direction == NE:
            tile = get_tile(board, (i - 1, j + 1))
        # East
        elif direction == E:
            tile = get_tile(board, (i, j + 1))
        # South-east
        elif direction == SE:
            tile = get_tile(board, (i + 1, j + 1))
        # South
        elif direction == S:
            tile = get_tile(board, (i + 1, j))
        # South-west
        elif direction == SW:
            tile = get_tile(board, (i + 1, j - 1))
        # West
        elif direction == W:
            tile = get_tile(board, (i, j - 1))
        # North-west
        elif direction == NW:
            tile = get_tile(board, (i - 1, j - 1))

        # Info
        # if (tile[1] is not None):
        #    print ("The tile {} of {} is {}.".format(
        #        direction.lower(), coords, tile))
        # else:
        #    print ("There is no tile {} of {}.".format(
        #        direction.lower(), coords))

    return tile


# Check 9-long row of tiles
def get_row(board, coords, direction):
    directions = []
    
    tile = get_tile(board, coords)

    # Horizontal
    if direction == H:
        directions.append(W)
        directions.append(E)
    # Vertical
    elif direction == V:
        directions.append(N)
        directions.append(S)
    # Left-diagonal
    elif direction == LD:
        directions.append(NW)
        directions.append(SE)
    # Right-diagonal
    elif direction == RD:
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


# [0, (4, 2)] to [0, (4, 10)]; Score: 8
def get_row_score(row, given_id):
    other_id = given_id * -1
    row_score = 0
    consec = 0
    for tile in row:
        if tile[0] == given_id:
            consec += 1
        if consec >= 4:
            row_score = math.inf
        elif tile[0] != given_id:
            if consec >= 4:
                row_score = math.inf
            elif tile[0] == other_id:
                pass
            elif consec > 0:
                row_score += int(math.pow(10, consec))
            elif tile[0] == EMPTY:
                row_score += 1
            consec = 0

    return row_score


def get_board_score(board, given_id):
    other_id = given_id * -1
    board_score = 0

    empty_tiles = get_empty_coords(board)

    for tile in empty_tiles:
        given_tile_score = get_tile_score(board, given_id, tile)
        other_tile_score = get_tile_score(board, other_id, tile)

        if given_tile_score == math.inf:
            return given_tile_score
        if other_tile_score == math.inf:
            return -math.inf

        value = given_tile_score[0] + other_tile_score[0]
        board_score += value

    return board_score


# TODO: Change so it predicted new value of tile
# Return score of tile
def get_tile_score(board, given_id, coords):
    copy_board = deepcopy(board)
    total_score = 0
    
    tile = get_tile(board, coords)
    value = tile[0]
    i, j = tile[1]

    if value == EMPTY:

        copy_board[i][j] = given_id
    else:
        return [0, coords]

    star = get_star(copy_board, coords)
    for x in range(len(star)):
        row = star[x]

        row_score = get_row_score(row, given_id)

        total_score += row_score
        
    # print ("Score for {} for player_id={}: {}".format(
    #    coords, player_id, total_score))

    return [total_score, coords]


def get_tile_scores(board, given_id):
    tiles = []
    empty_coords = get_empty_coords(board)

    for coords in empty_coords:
        tile = get_tile_score(board, given_id, coords)
        tiles.append(tile)

    tiles = sorted(tiles, key=lambda k: k[0], reverse=True)

    return tiles


def get_best_moves(board, given_id, amount):
    best_moves = []

    all_best_moves = get_tile_scores(board, given_id)

    for i in range(amount):
        best_move = all_best_moves.pop(0)
        best_moves.append(best_move)

    return best_moves


# Analyse player
def get_best_move(board, given_id):
    other_id = given_id * -1

    given_tile_scores = get_tile_scores(board, given_id)
    other_tile_scores = get_tile_scores(board, other_id)

    best_given_move = given_tile_scores[0]
    best_other_move = other_tile_scores[0]

    print("Best move for {}: {}\nBest move for {}: {}".format(
        given_id,
        best_given_move,
        other_id,
        best_other_move))

    if best_given_move > best_other_move:
        best_move = best_given_move
    else:
        best_move = best_other_move

    return best_move


# Returns a list of the 5 tiles from the given coordinate, with the given tile at the start of the list. If there are no
# tiles to add, the list will be returned as it is.
# @direction = N, NE, E, SE, S, SW, W, NW
def get_row2(board, coord, direction):
    row = []

    tile = get_tile(board, coord)

    row.append(tile)
    for i in range(4):
        next_tile = look(board, row[i][1], direction)
        row.append(next_tile)

    final_row = []
    for i in range(len(row)):
        if row[i] != [None, None]:
            final_row.append(row[i])

    return final_row


# Returns a list of the amount of rows a tile can make. For example, [2, 1, 1, 1, 1] means the given player can make
# 2 fives, 1 four, 1 three, 1 two, and 1 one.
# NOTE: Enter a coordinate that is an empty tile.
def get_row_amounts(board, coord, given_id):
    copyboard = deepcopy(board)
    amounts = [0, 0, 0, 0, 0]

    tile = get_tile(board, coord)
    value = tile[0]
    i, j = coord

    # If value is an empty tile, then make it so the given player's tile is there
    if value == given_id * -1:
        return amounts

    elif value == EMPTY:
        copyboard[i][j] = given_id

    for direction in DIRECTIONS:
        row = get_row2(copyboard, coord, direction)
        consec = 0

        for cur_tile in row:
            value = cur_tile[0]
            if value == given_id:
                consec += 1
            else:
                break

        if consec == 1:
            amounts[5 - consec] = 1
        else:
            amounts[5 - consec] += 1

    return amounts


#
def get_board_amounts(board, given_id):
    empty_coords = get_empty_coords(board)
    total_amounts = [0, 0, 0, 0, 0]

    for coord in empty_coords:
        tile_row_amounts = get_row_amounts(board, coord, given_id)

        for i in range(len(tile_row_amounts)):
            total_amounts[i] += tile_row_amounts[i]

    return total_amounts


def create_board_score(board, given_id):
    row_data = get_board_amounts(board, given_id)

    twos_score = row_data[3] * 8
    threes_score = row_data[2] * (8**4)
    fours_score = row_data[1] * (8**8)
    fives_score = row_data[0] * (8**16)
    board_score = fives_score + fours_score + threes_score + twos_score
    return board_score


# The player will always be the one maximising
def minimax(board, depth, given_id, alpha=-math.inf, beta=math.inf, curr_child=None):
    board_copy = deepcopy(board)
    other_id = given_id * -1

    if depth == 0 or winningTest(given_id, board_copy, 5):
        return curr_child

    children = get_best_moves(board_copy, given_id, 4)

    # Maximising player
    if given_id == player_id:
        max_score = -math.inf
        max_child = None
        for child in children:
            y_coord = child[1][0]
            x_coord = child[1][1]
            board_copy[y_coord][x_coord] = given_id
            minimax(board_copy, depth-1, other_id, alpha, beta, child)
            board_score = create_board_score(board_copy, given_id)
            if board_score > max_score:
                max_score = board_score
                max_child = child
            alpha = max(alpha, board_score)
            if beta <= alpha:
                break
        return max_child
    else:
        min_score = math.inf
        min_child = None
        for child in children:
            y_coord = child[1][0]
            x_coord = child[1][1]
            board_copy[y_coord][x_coord] = other_id
            minimax(board_copy, depth-1, other_id, alpha, beta, child)
            board_score = create_board_score(board, other_id)
            if board_score < min_score:
                min_score = board_score
                min_child = child
            beta = min(beta, board_score)
            if beta <= alpha:
                break
        return min_child
