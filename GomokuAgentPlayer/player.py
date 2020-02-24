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
            
        opponent_tiles = get_opponent_tiles(board, opponent_id)
        opponent_tiles.sort()
        
        empty_tiles = get_empty_tiles(board)
        
        split_threes = look_for_lines(board, opponent_tiles, 4, 4, True)
        split_fours = look_for_lines(board, opponent_tiles, 5, 5, True)
        open_threes = look_for_lines(board, opponent_tiles, 3, 3, False)
        open_fours = look_for_lines(board, opponent_tiles, 4, 4, False)

        best_coord = choose_loc(open_threes, open_fours, split_threes, split_fours, board)
        
        if (check_centre(board) is not None):
            print ("Centre tile free.")
            best_coord = check_centre(board)

        else:
            if best_coord is None or best_coord == 0:
                print("No best move. Choosing random coordinate...")
                best_coord =  move_randomly(self, board)
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
        print ("Move loc:", move_loc)
        if legalMove(board, move_loc):
            return move_loc


# Returns centre tile coords if empty and None otherwise
def check_centre(board):
    size = len(board)
    mid = size // 2

    mid_tile = (mid, mid)

    if (legalMove(board, mid_tile)):
        return mid_tile

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
        end_pos = line_to_extract[len(line_to_extract)-1]
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
            if start_pos[0] < len(local_board[0])-1 and start_pos[1] > 0:
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


#(?)  TEMP METHOD: Prints out lines.
def print_lines(lines):
    for line in lines:
        print(line)


# Returns the opponents ID. Only called once per game.
def get_opponent_id(board):
    for row in board:
        for tile in row:
            if tile != player_id and tile != 0:
                return tile


# Returns the co-ordinates of the opponent tiles
def get_opponent_tiles(board, other_id):
    coords = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == other_id:
                coords.append([i, j])
    return coords


# Returns the co-ordinates of all player tiles
def get_player_tiles(board, player_id):
    coords = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == player_id:
                coords.append([i, j])
    return coords


# Returns the co-ordinates of all empty  tiles
def get_empty_tiles(board):
    coords = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                coords.append([i, j])
    return coords



# TODO: Sort this cluster-fuck out.
# this looks at the opponents tiles and returns you any lines between the min and max size
# to find just split rows of 3, a min and max size of four would be needed and gap_allowed would need to be true.
# TODO this is ridiculous, can be cut down by generalising and creating smaller functions, not priority right now.
# TODO say you are looking for open 4's and there is an arrangement 1011101, it will only find the first one
def look_for_lines(board, opponent_tiles, min_size, max_size, gap_allowed=False):
    lines = []
    lines_dic = {
        HORIZONTAL: [],
        VERTICAL: [],
        DIAG_BOT_LEFT: [],
        DIAG_TOP_LEFT: []
    }
    lines_with_gap_dic = {
        HORIZONTAL: [],
        VERTICAL: [],
        DIAG_BOT_LEFT: [],
        DIAG_TOP_LEFT: []
    }
    for tile in opponent_tiles:
        poss_tiles_horizontal = []
        poss_tiles_vertical = []
        # we need to make two diagonal list to make sure rows are formed properly
        # this list starts from the bottom left and goes to top right
        poss_tiles_diag_1 = []
        # this list starts from the top left and goes to the bottom right
        poss_tiles_diag_2 = []

        # STARTING HORIZONTAL SEARCH
        # first we look left
        curr_tile = tile.copy()
        for i in range(max_size-1):
            curr_tile = look(curr_tile, LEFT)
            if curr_tile[1] > -1:
                poss_tiles_horizontal.append(curr_tile.copy())

        # now we look right
        curr_tile = tile.copy()
        for i in range(max_size-1):
            curr_tile = look(curr_tile, RIGHT)
            if curr_tile[1] < len(board[0]):
                poss_tiles_horizontal.append(curr_tile.copy())

        # STARTING VERTICAL SEARCH
        # now we look up
        curr_tile = tile.copy()
        for i in range(max_size - 1):
            curr_tile = look(curr_tile, UP)
            if curr_tile[0] > 0:
                poss_tiles_vertical.append(curr_tile.copy())

        # now we look down
        curr_tile = tile.copy()
        for i in range(max_size - 1):
            curr_tile = look(curr_tile, DOWN)
            if curr_tile[0] < len(board):
                poss_tiles_vertical.append(curr_tile.copy())

        # STARTING DIAGONAL SEARCH
        # now we look down and left
        curr_tile = tile.copy()
        for i in range(max_size - 1):
            curr_tile = look(curr_tile, DOWN)
            curr_tile = look(curr_tile, LEFT)
            if curr_tile[0] < len(board) and curr_tile[1] > 0:
                poss_tiles_diag_1.append(curr_tile.copy())

        # now we look up and right
        curr_tile = tile.copy()
        for i in range(max_size - 1):
            curr_tile = look(curr_tile, UP)
            curr_tile = look(curr_tile, RIGHT)
            if curr_tile[0] > 0 and curr_tile[1] < len(board[0]):
                poss_tiles_diag_1.append(curr_tile.copy())

        # now we look up and left
        curr_tile = tile.copy()
        for i in range(max_size - 1):
            curr_tile = look(curr_tile, UP)
            curr_tile = look(curr_tile, LEFT)
            if curr_tile[0] > 0 and curr_tile[1] > 0:
                poss_tiles_diag_2.append(curr_tile.copy())

        # now we look down and right
        curr_tile = tile.copy()
        for i in range(max_size - 1):
            curr_tile = look(curr_tile, DOWN)
            curr_tile = look(curr_tile, RIGHT)
            if curr_tile[0] < len(board) and curr_tile[1] < len(board[0]):
                poss_tiles_diag_2.append(curr_tile.copy())

        # append the original tile for both lists
        poss_tiles_horizontal.append(tile.copy())
        poss_tiles_vertical.append(tile.copy())
        poss_tiles_diag_1.append(tile.copy())
        poss_tiles_diag_2.append(tile.copy())

        # now to check all of these tiles for connected lines
        # these must be sorted so elements are gone through in order
        poss_tiles_horizontal.sort()
        poss_tiles_vertical.sort()
        poss_tiles_diag_1.sort()
        poss_tiles_diag_2.sort()
        curr_line = []

        if gap_allowed:
            gap_used = False
        else:
            gap_used = True
        for poss_tile in poss_tiles_horizontal:
            if is_in(poss_tile, opponent_tiles) or (gap_used is False and board[poss_tile[0]][poss_tile[1]] == 0):
                if not is_in(poss_tile, opponent_tiles):
                    gap_used = True
                curr_line.append(poss_tile)
            else:
                if len(curr_line) >= min_size and curr_line not in lines:
                    if curr_line[0] != 0 and curr_line[len(curr_line)-1] != 0:
                        lines.append(curr_line.copy())
                        lines_dic[HORIZONTAL].append(curr_line.copy())
                curr_line.clear()
                if gap_allowed:
                    gap_used = False

        curr_line.clear()
        if gap_allowed:
            gap_used = False
        else:
            gap_used = True
        for poss_tile in poss_tiles_vertical:
            if is_in(poss_tile, opponent_tiles) or (gap_used is False and board[poss_tile[0]][poss_tile[1]] == 0):
                if not is_in(poss_tile, opponent_tiles):
                    gap_used = True
                curr_line.append(poss_tile)
            else:
                if len(curr_line) >= min_size and curr_line not in lines:
                    if curr_line[0] != 0 and curr_line[len(curr_line)-1] != 0:
                        lines.append(curr_line.copy())
                        lines_dic[VERTICAL].append(curr_line.copy())
                curr_line.clear()
                if gap_allowed:
                    gap_used = False

        curr_line.clear()
        if gap_allowed:
            gap_used = False
        else:
            gap_used = True
        for poss_tile in poss_tiles_diag_1:
            if is_in(poss_tile, opponent_tiles) or (gap_used is False and board[poss_tile[0]][poss_tile[1]] == 0):
                if not is_in(poss_tile, opponent_tiles):
                    gap_used = True
                curr_line.append(poss_tile)
            else:
                if len(curr_line) >= min_size and curr_line not in lines:
                    if curr_line[0] != 0 and curr_line[len(curr_line)-1] != 0:
                        lines.append(curr_line.copy())
                        lines_dic[DIAG_BOT_LEFT].append(curr_line.copy())
                curr_line.clear()
                if gap_allowed:
                    gap_used = False

        curr_line.clear()
        if gap_allowed:
            gap_used = False
        else:
            gap_used = True
        for poss_tile in poss_tiles_diag_2:
            if is_in(poss_tile, opponent_tiles) or (gap_used is False and board[poss_tile[0]][poss_tile[1]] == 0):
                if not is_in(poss_tile, opponent_tiles):
                    gap_used = True
                curr_line.append(poss_tile)
            else:
                if len(curr_line) >= min_size and curr_line not in lines:
                    if curr_line[0] != 0 and curr_line[len(curr_line)-1] != 0:
                        lines.append(curr_line.copy())
                        lines_dic[DIAG_TOP_LEFT].append(curr_line.copy())
                curr_line.clear()
                if gap_allowed:
                    gap_used = False

    for option in lines_dic:
        lines = lines_dic[option]
        for line in lines:
            first_pos = board[line[0][0]][line[0][1]]
            last_pos = board[line[len(line)-1][0]][line[len(line)-1][1]]
            if first_pos == 0 or last_pos == 0:
                lines.remove(line)
            elif np.isin(0, line):
                lines_with_gap_dic[option].append(line)
                lines_dic[option].remove(line)
    if gap_allowed:
        return lines_with_gap_dic
    else:
        return lines_dic


# Checks if an element is in a list of elements. Used for comparing lists of lists (due to the fact it's more complicated than np.isin()).
def is_in(element, list_of_elements):
    for list_element in list_of_elements:
        if np.equal(list_element, element).all():
            return True
    return False


# Takes in a tile location and direction and looks one square in that specified direction.
def look(tile, direction):
    if direction == LEFT:
        new_tile = tile
        new_tile[1] = new_tile[1] - 1
        return new_tile
    if direction == RIGHT:
        new_tile = tile
        new_tile[1] = new_tile[1] + 1
        return new_tile
    if direction == UP:
        new_tile = tile
        new_tile[0] = new_tile[0] - 1
        return new_tile
    if direction == DOWN:
        new_tile = tile
        new_tile[0] = new_tile[0] + 1
        return new_tile
