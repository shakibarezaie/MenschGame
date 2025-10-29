from typing import Tuple

from .import colors



COLOR_MAPPING = {
    0: colors.COLOR_RED,
    1: colors.COLOR_BLUE,
    2: colors.COLOR_GREEN,
    3: colors.COLOR_YELLOW
}

LIGHT_COLOR_MAPPING = {
    0: colors.COLOR_LIGHT_RED,
    1: colors.COLOR_LIGHT_BLUE, 
    2: colors.COLOR_LIGHT_GREEN, 
    3: colors.COLOR_LIGHT_YELLOW
}



def get_home_positions(): 
    return [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(9, 0), (10, 0), (9, 1), (10, 1)],
        [(9, 9), (10, 9), (9, 10), (10, 10)],
        [(0, 9), (1, 9), (0, 10), (1, 10)],
    ]

def get_starting_positions(): 
    return [
        [(0, 4)],
        [(6, 0)], 
        [(10, 6)], 
        [(4, 10)]
    ]

def get_safe_postions(): 
    return [
        [(1, 5), (2, 5), (3, 5), (4, 5)],
        [(5, 1), (5, 2), (5, 3), (5, 4)],
        [(6, 5), (7, 5), (8, 5), (9, 5)],
        [(5, 6), (5, 7), (5, 8), (5, 9)],
    ]

def get_white_cells_postions():
    # relative to red positions. 
    return [[(1, 4), (2, 4), (3, 4), (4, 4), 
            (4, 3), (4, 2), (4, 1), (4, 0),
            (5, 0),
            (6, 1), (6, 2), (6, 3), (6, 4),
            (7, 4), (8, 4), (9, 4), (10, 4), 
            (10, 5),
            (9, 6), (8, 6), (7, 6), (6, 6),
            (6, 7), (6, 8), (6, 9), (6, 10),
            (5, 10),
            (4, 9), (4, 8), (4, 7), (4, 6),
            (3, 6), (2 , 6), (1, 6), (0, 6),
            (0, 5)
    ]]



def get_position(
        player_number: int, 
        piece_number: int, 
        state_position: int
) -> Tuple[int, int]:
    if state_position == -6:
        return get_home_positions()[player_number][piece_number]
    
    if 1 <= state_position <= 36:
        return get_white_cells_postions()[0][
            (state_position - 1 + player_number * 9) % 36
        ]

    if 37 <= state_position <= 40:
        return get_safe_postions()[player_number][state_position-37]
    
    if state_position == 0: 
        return get_starting_positions()[player_number][0]
    