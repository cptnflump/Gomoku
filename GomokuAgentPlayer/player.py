import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent

opponent_id = 0
priority_moves_queue = []
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


class Player(GomokuAgent):
    def move(self, board):
        global opponent_id
        if opponent_id == 0:
            opponent_id = get_opponent_id(board, self.ID)
            print("opponent id is: " + str(opponent_id))
        while True:
            opponent_tiles = observe_opponent_tiles(board, opponent_id)
            opponent_tiles.sort()
            lines = look_for_lines(board, opponent_tiles, 3, 4)
            print_lines(lines)
            move_loc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            print("Placing a tile at: " + str(move_loc))
            if legalMove(board, move_loc):
                return move_loc


# temp method just for printing lines as np.matrix() didn't work
def print_lines(lines):
    for line in lines:
        print(line)


# this retrieves the id of the opponent for checking state in the future, only done once per game
def get_opponent_id(board, player_id):
    for row in board:
        for tile in row:
            if tile != player_id and tile != 0:
                return tile


# this looks at the board and returns the coordinates for every opponent tile
def observe_opponent_tiles(board, other_id):
    coords = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == other_id:
                coords.append([i, j])
    return coords


# this looks at the opponents tiles and returns you any lines between the min and max size
def look_for_lines(board, opponent_tiles, min_size, max_size):
    lines = []
    for tile in opponent_tiles:
        poss_tiles_horizontal = []
        poss_tiles_vertical = []

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

        # append the original tile for both lists
        poss_tiles_horizontal.append(tile.copy())
        poss_tiles_vertical.append(tile.copy())

        # now to check all of these tiles for connected lines
        poss_tiles_horizontal.sort()
        poss_tiles_vertical.sort()
        curr_line = []
        for poss_tile in poss_tiles_horizontal:
            if is_in(poss_tile, opponent_tiles):
                curr_line.append(poss_tile)
            else:
                if len(curr_line) >= min_size and curr_line not in lines:
                    lines.append(curr_line.copy())
                curr_line.clear()
        curr_line.clear()
        for poss_tile in poss_tiles_vertical:
            if is_in(poss_tile, opponent_tiles):
                curr_line.append(poss_tile)
            else:
                if len(curr_line) >= min_size and curr_line not in lines:
                    lines.append(curr_line.copy())
                curr_line.clear()
    return lines


# checks if an element is in a list of elements, for comparing lists of lists as it is more complicated than np.isin()
def is_in(element, list_of_elements):
    for list_element in list_of_elements:
        if np.equal(list_element, element).all():
            return True
    return False


# not implemented
def look_for_split_groups(board, opponent_tiles, size):
    return None


# this takes in a tile location and looks one square in the specified direction
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
