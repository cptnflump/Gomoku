#######################################################
# Gomoku Agent
# Version 1.2.1
#
# Jake Smith, Jacob Roberts
# Student Numbers: 901519, 913408
# Swansea University
# March 2020
#

# Imports
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
        print("\n")
        global opponent_id
        global player_id
        global move_count

        # Player and opponent ID assignment
        player_id = self.ID
        opponent_id = get_opponent_id(board)

        # Move count
        move_count += 1

        player_best_move = None

        # First we check for opponent rows of three or four to block as highest priority
        # If there are no rows that need to be blocked it will look to play it's own fours or fives
        # If there are no high priority moves to make (threes and fours), we run Minimax to give us the best position
        # In this case Minimax looks four moves ahead, looking at four possible beneficial moves
        try:
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
                player_best_move = Minimax(board, 4, self.ID)[1]
        # An IndexError can occur in the case that the AI cannot find a beneficial move to make
        # This occurs generally at the end of game in which the board is nearly full
        except IndexError:
            coords = get_empty_coords(board)
            player_best_move = coords[0]

        return player_best_move


# Returns centre tile coords if empty and None otherwise
def check_centre(board):
    size = len(board)
    mid = size // 2
    mid_tile = (mid, mid)
    if legalMove(board, mid_tile):
        return mid_tile


# Returns the ID of the opponent
def get_opponent_id(board):
    for row in board:
        for tile in row:
            if tile != player_id and tile != 0:
                return tile

    return player_id * -1


# Returns all the coordinates from the board that are empty
def get_empty_coords(board):
    coords = []
    for i in range(len(board)):
        for j in range(len(board)):
            tile = get_tile(board, (i, j))
            if tile[0] == EMPTY:
                coords.append(tile[1])
    return coords


# Returns the value and set of coordinates for a given tile
def get_tile(board, coords):
    size = len(board)
    i, j = coords[0], coords[1]

    if 0 <= i < size and 0 <= j < size:
        value = board[i][j]
        tile = [value, coords]
        return tile
    else:
        return [None, None]


# Given a set of coordinates and a direction, returns the next tile over in that direction
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

    return tile


# Returns a list of tiles with the given tile at the centre of the list. If any None values are found, they are removed
# from the list.
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

    # Removing None values from the list
    final_row = []
    for i in range(len(row)):
        if row[i] != [None, None]:
            final_row.append(row[i])
    
    return final_row


# Return a list of each row around a given tile (horizontal, vertical, left-diagonal, and right-diagonal).
def get_star(board, coords):
    star = []
    directions = [H, V, LD, RD]

    for direction in directions:
        row = get_row(board, coords, direction)
        star.append(row)

    return star


# Return the score of a given row
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


# Return the score of a given tile
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

    return [total_score, coords]


# Returns the score of every empty tile on the board
def get_tile_scores(board, given_id):
    tiles = []
    empty_coords = get_empty_coords(board)

    for coords in empty_coords:
        tile = get_tile_score(board, given_id, coords)
        tiles.append(tile)

    tiles = sorted(tiles, key=lambda k: k[0], reverse=True)

    return tiles


# Returns the n best moves of a given player
def get_best_moves(board, given_id, amount):
    best_moves = []

    all_best_moves = get_tile_scores(board, given_id)

    for i in range(amount):
        best_move = all_best_moves.pop(0)
        best_moves.append(best_move)

    return best_moves


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


# Returns the number of 5s, 4s, etc. that can be made on the board
def get_board_amounts(board, given_id):
    empty_coords = get_empty_coords(board)
    total_amounts = [0, 0, 0, 0, 0]

    for coord in empty_coords:
        tile_row_amounts = get_row_amounts(board, coord, given_id)

        for i in range(len(tile_row_amounts)):
            total_amounts[i] += tile_row_amounts[i]

    return total_amounts


# This looks at the board from the perspective of a given player
# A score is generated based on the number of possible (not already formed) 2's, 3's, 4's and 5's on the board
# Larger possible rows are scored much higher
# This is use in the Minimax algorithm to determine an overall score for a potential move
def create_board_score(board, given_id):
    row_data = get_board_amounts(board, given_id)

    twos_score = row_data[3] * 8
    threes_score = row_data[2] * (8**4)
    fours_score = row_data[1] * (8**8)
    fives_score = row_data[0] * (8**16)
    board_score = fives_score + fours_score + threes_score + twos_score
    return board_score


# This function is the implementation of the Minimax algorithm.
# This algorithm takes a state (board) and maximising player
# With this information, a number of possible moves from the current state are created (4 in this case)
# To help increase the efficiency of this algorithm. Alpha Beta Pruning has been implemented.
# Alpha Beta pruning speeds up Minimax by discarding sub-trees that do not need to be searched.
def Minimax(board, depth, given_id, alpha=-math.inf, beta=math.inf, curr_child=None):
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
            Minimax(board_copy, depth-1, other_id, alpha, beta, child)
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
            Minimax(board_copy, depth-1, other_id, alpha, beta, child)
            board_score = create_board_score(board, other_id)
            if board_score < min_score:
                min_score = board_score
                min_child = child
            beta = min(beta, board_score)
            if beta <= alpha:
                break
        return min_child