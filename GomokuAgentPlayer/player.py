# Imports
import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent

# Variables
opponent_id = 0
player_id = 0
priority_moves_queue = []

# Constants
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
VERTICAL = "vertical"
HORIZONTAL = "horizontal"
DIAG_BOT_LEFT = "diag_bot_left"
DIAG_TOP_LEFT = "diag_top_left"


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
        best_coord = get_best_move(board, player_id)

        # TODO: Essentially for the early game. Add to get_best_move    
        # if (check_centre(board) is not None):
        #     print ("Centre tile free.")
        #     best_coord = check_centre(board)

        if best_coord is None or best_coord == 0:
            print("No best move. Choosing random coordinate...")
            best_coord = move_randomly(self, board)
        elif not legalMove(board, best_coord):
            print("Illegal move made. Choosing random coordinate...")
            best_coord = move_randomly(self, board)
        # print("Choosing coord based on opponent placements.")

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


# Returns all the coordinates from the board
def get_all_coords(board):
    coords = []
    for i in range(len(board)):
        for j in range(len(board)):
            tile = get_tile(board, (i, j))
            coords.append(tile[1])
    return coords


# Given a board and a set of coordinates, returns the value and coordinates of a tile
def get_tile(board, coords):
    if coords is None:
        return None, None

    i, j = coords[0], coords[1]
    if i < 0 or i > len(board) - 1 or j < 0 or j > len(board) - 1:
        return None, None
    # print ("The tile at {} is {}.".format(tile, board[i][j]))
    value = board[i][j]
    return value, (i, j)


# Directions - this can definitely be condensed but used for ease of action
# TODO: Convert this into function similar to look
# Given a board and set of coordinates, returns the value and coordinates of the left tile
# If the tile does not exist, NONE is returned
def get_left(board, coords):
    if coords is None:
        return None, None

    i, j = coords[0], coords[1] - 1
    if j < 0:
        return None, None
    else:
        return get_tile(board, [i, j])


# Returns a list containing the value and coordinates of the tile right of a given tile
# None is returned if the tile does not exist
def get_right(board, coords):
    if coords is None:
        return None, None

    i, j = coords[0], coords[1] + 1
    if j > len(board) - 1:
        # print ("There is no tile right of {}.".format(tile))
        return None, None
    else:
        return get_tile(board, [i, j])


# Returns a list containing the value and coordinates of the tile above of a given tile
# None is returned if the tile does not exist
def get_up(board, coords):
    if coords is None:
        return None, None

    i, j = coords[0] - 1, coords[1]
    if j < 0:
        # print ("There is no tile above of {}.".format(tile))
        return None, None
    else:
        return get_tile(board, [i, j])


# Returns a list containing the value and coordinates of the tile below of a given tile
# None is returned if the tile does not exist
def get_down(board, coords):
    if coords is None:
        return None, None

    i, j = coords[0] + 1, coords[1]
    if j > len(board) - 1:
        # print ("There is no tile below of {}.".format(tile))
        return None, None
    else:
        return get_tile(board, [i, j])


# Returns a list containing the value and coordinates of the tile top-left of a given tile
# None is returned if the tile does not exist
def get_topleft(board, coords):
    if coords is None:
        return None, None

    i, j = coords[0] - 1, coords[1] - 1
    if j < 0 or i < 0:
        return None, None
    else:
        return get_tile(board, [i, j])


# Returns a list containing the value and coordinates of the tile top-right of a given tile
# None is returned if the tile does not exist
def get_topright(board, coords):
    if coords is None:
        return None, None

    i, j = coords[0] - 1, coords[1] + 1
    if i < 0 or j > len(board) - 1:
        return None, None
    else:
        return get_tile(board, [i, j])


# Returns a list containing the value and coordinates of the tile bottom-left of a given tile
# None is returned if the tile does not exist
def get_botleft(board, coords):
    if coords is None:
        return None, None
    i, j = coords[0] + 1, coords[1] - 1
    if i > len(board) - 1 or j < 0:
        return None, None
    else:
        return get_tile(board, [i, j])


# Returns a list containing the value and coordinates of the tile top-left of a given tile
# None is returned if the tile does not exist
def get_botright(board, coords):
    if coords is None:
        return None, None

    i, j = coords[0] + 1, coords[1] + 1
    if i > len(board) - 1 or j > len(board) - 1:
        return None, None
    else:
        return get_tile(board, [i, j])


# Rows - functions for returning row of FIVE tiles with given coordinates in the centre.
# TODO: Thinking of expanding FIVE to SEVEN to increase accuracy?
# Returns list of lists [[value, (i, j)]] of values and coords in horizontal row from a given tile
def get_hrow(board, coords):
    current_tile = get_tile(board, coords)
    left = get_left(board, coords)
    right = get_right(board, coords)

    left2 = get_left(board, left[1])
    right2 = get_right(board, right[1])

    row = [left2, left, current_tile, right, right2]

    sum_of_row = 0
    for value in row:
        if value is None:
            pass
        elif value[0] == 1:
            sum_of_row += 1

    return row


# Returns list of lists [[value, (i, j)]] of values and coords in vertical row from a given tile
def get_vrow(board, coords):
    current_tile = get_tile(board, coords)
    up = get_up(board, coords)
    down = get_down(board, coords)

    up2 = get_up(board, up[1])
    down2 = get_down(board, down[1])

    row = [up2, up, current_tile, down, down2]

    sum_of_row = 0
    for value in row:
        # print (value)
        if value is None:
            pass
        elif value[0] == 1:
            sum_of_row += 1

    return row


# Returns list of lists [[value, (i, j)]] of values and coords from top left to bot right from a given tile
def get_ldiag(board, coords):
    current_tile = get_tile(board, coords)
    top_left = get_topleft(board, coords)
    bot_right = get_botright(board, coords)

    top_left2 = get_topleft(board, top_left[1])
    bot_right2 = get_botright(board, bot_right[1])

    row = [top_left2, top_left, current_tile, bot_right, bot_right2]

    sum_of_row = 0
    for value in row:
        # print (value)
        if value is None:
            pass
        elif value[0] == 1:
            sum_of_row += 1

    return row


# Returns list of lists [[value, (i, j)]] of values and coords from top right to bot left from a given tile
def get_rdiag(board, coords):
    # print ("Tile selected: {}.".format(tile))

    current_tile = get_tile(board, coords)
    top_right = get_topright(board, coords)
    bot_left = get_botleft(board, coords)

    top_right2 = get_topright(board, top_right[1])
    bot_left2 = get_botleft(board, bot_left[1])

    row = [top_right2, top_right, current_tile, bot_left, bot_left2]

    sum_of_row = 0
    for value in row:
        # print (value)
        if value is None:
            pass
        elif value[0] == 1:
            sum_of_row += 1

    return row


# Returns list of lists [[value, (i, j)]] of values and coords in each direction
def get_star(board, coords):
    horizontal = get_hrow(board, coords)
    vertical = get_vrow(board, coords)
    left_diag = get_ldiag(board, coords)
    right_diag = get_rdiag(board, coords)

    sum_of_star = (get_sum(horizontal, 1) +
                   get_sum(vertical, 1) +
                   get_sum(left_diag, 1) +
                   get_sum(right_diag, 1))

    return [horizontal, vertical, left_diag, right_diag]


# Return sum of values from list of values and coordinates
def get_sum(row, expected_id):
    total = 0
    for tile in row:
        value = tile[0]
        if value is None:
            total += 0
        elif value == expected_id:
            total += (expected_id * value)

    return total


# Return sum of values from list of values and coordinates
# Not currently used but might have future use by determining the 'value' of a move
def get_sum_of_star(board, tile, expected_id):
    star = get_star(board, tile)
    total = 0
    for row in star:
        sum_of_row = get_sum(row, expected_id)
        total += sum_of_row

    return total


# Analyse player
# Returns fours and threes of a given player
def analyse_player(board, expected_id):
    print("Analysing player_id: {}\nAnalysing...\n".format(expected_id))
    fours = []
    threes = []
    twos = []
    board_coords = get_all_coords(board)

    for coords in board_coords:
        star = get_star(board, coords)
        for row in star:
            sum_of_row = get_sum(row, expected_id)
            if sum_of_row == 4:
                print("WARNING: Row of four found:")
                print(row)
                for tile in row:
                    if tile[0] == 0:
                        print("Block at {}".format(tile[1]))
                        fours.append(tile[1])
            if sum_of_row == 3:
                print("Row of three found:")
                print(row)
                for tile in row:
                    if tile[0] == 0:
                        print("Block at {}".format(tile[1]))
                        threes.append(tile[1])

    fours.sort(key=lambda k: [k[0], k[1]])

    threes = sorted(threes, key=threes.count, reverse=True)

    if len(fours) == 0:
        print("This player has no winning moves.")
    else:
        print("Fours (URGENT): {}".format(fours))

    if len(threes) == 0:
        print("This player has no threes.")
    else:
        print("Threes (Warning!): {}".format(threes))

    return fours, threes


# Returns coordinates of best move
def get_best_move(board, expected_id):
    print("Calculating best move for player_id: {}".format(expected_id))

    best_move = None
    opponent_fours, opponent_threes = analyse_player(board, opponent_id)
    player_fours, player_threes = analyse_player(board, player_id)

    # If player has winning move
    if len(player_fours) > 0:
        best_move = player_fours[0]
    # If opponent has winning move
    elif len(opponent_fours) > 0:
        best_move = opponent_fours[0]
    # If player has three
    elif len(player_threes) > 0:
        best_move = player_threes[0]
    # If opponent has three
    elif len(player_threes) > 0:
        best_move = opponent_threes[0]

    # MORE TO ADD TO INCREASE ACCURACY

    print("The best move for player_id: {} is {}".format(expected_id, best_move))
    return best_move


# TODO this is semi functioning, it needs to start checking for a 0 in the return space
def choose_loc(open_threes, open_fours, split_threes, split_fours, board):
    local_board = board.copy()
    direction = None
    is_split = False
    used_list = []
    if any(value != [] for value in split_fours.values()):
        used_dic = split_fours
        is_split = True
    elif any(value != [] for value in open_fours.values()):
        used_dic = open_fours
    elif any(value != [] for value in split_threes.values()):
        used_dic = split_threes
        is_split = True
    elif any(value != [] for value in open_threes.values()):
        used_dic = open_threes
    else:
        return None
    print("USED DIC: " + str(used_dic))
    for direction_list in used_dic:
        if used_dic[direction_list]:
            used_list = used_dic[direction_list]
            direction = direction_list
    print("DIRECTON " + direction)
    line_to_extract = used_list[0]
    print("LINE TO EXTRACT " + str(line_to_extract))
    print("IS SPLIT: " + str(is_split))
    if is_split:
        for pos in line_to_extract:
            print(local_board[pos[0]][pos[1]])
            if local_board[pos[0]][pos[1]] == 0:
                return tuple(pos)
    else:
        start_pos = line_to_extract[0]
        end_pos = line_to_extract[len(line_to_extract) - 1]
        if direction == HORIZONTAL:
            if start_pos[1] > 0:
                return_pos = start_pos
                return_pos[1] = start_pos[1] - 1
            else:
                return_pos = end_pos
                return_pos[1] = end_pos[1] + 1
        elif direction == VERTICAL:
            if start_pos[0] > 0:
                return_pos = start_pos
                return_pos[0] = start_pos[0] - 1
            else:
                return_pos = end_pos
                return_pos[0] = end_pos[0] + 1
        elif direction == DIAG_BOT_LEFT:
            if start_pos[0] < len(local_board[0]) - 1 and start_pos[1] > 0:
                return_pos = start_pos
                return_pos[0] = start_pos[0] - 1
                return_pos[1] = start_pos[1] + 1
            else:
                return_pos = end_pos
                return_pos[0] = start_pos[0] + 1
                return_pos[1] = start_pos[1] - 1
        elif direction == DIAG_TOP_LEFT:
            if start_pos[0] > 0 and start_pos[1] > 0:
                return_pos = start_pos
                return_pos[0] = start_pos[0] - 1
                return_pos[1] = start_pos[1] - 1
            else:
                return_pos = end_pos
                return_pos[0] = end_pos[0] + 1
                return_pos[1] = end_pos[1] + 1
        else:
            return None
        print(return_pos)
        return tuple(return_pos)


# (?)  TEMP METHOD: Prints out lines.
def print_lines(lines):
    for line in lines:
        print(line)


# Returns the opponents ID. Only called once per game.
def get_opponent_id(board):
    for row in board:
        for tile in row:
            if tile != player_id and tile != 0:
                return tile


def look(board, tile, direction):
    size = len(board)
    new_tile = None

    if direction == UP:
        new_tile = tile
        if new_tile[0] - 1 < 0:
            return None
        else:
            new_tile[0] -= 1

    if direction == DOWN:
        new_tile = tile
        if new_tile[0] + 1 >= size:
            return None
        else:
            new_tile[0] += 1

    if direction == LEFT:
        new_tile = tile
        if tile[1] - 1 < 0:
            return None
        else:
            new_tile[1] -= 1

    if direction == RIGHT:
        new_tile = tile
        if tile[1] + 1 >= size:
            return None
        else:
            new_tile[1] += 1

    return new_tile

