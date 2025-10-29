import random 
from typing import List, Optional, Tuple

class InvalidMove(Exception):
    pass

# -6 (home),
# 0 (starting position), 
# 1 ... 36 white positions,
# 37 ... 40 (safe position)

# postions are relatively stored.

PLAYERS = [
    [-6, -6, -6, -6], # red
    [-6, -6, -6, -6], # blue
    [-6, -6, -6, -6], # green
    [-6, -6, -6, -6], # yellow
]

START_POSITION = 0
WHITE_START = 1
WHITE_END = 36
SAFE_START = 37
SAFE_END = 40

CURRENT_PLAYER = 0



def roll_dice() -> int:
    return random.randint(1, 6)

def _is_six_rolled(dice_number: int) -> bool:
    return dice_number == 6

def next_turn(dice_number): 
    global CURRENT_PLAYER

    if not _is_six_rolled(dice_number):
        CURRENT_PLAYER = (CURRENT_PLAYER + 1) % 4



def get_current_player() -> int:
    global CURRENT_PLAYER
    return CURRENT_PLAYER

def get_players_state() -> List[List[int]]:
    global PLAYERS
    return PLAYERS



def _is_piece_selectable(position: int, dice_number: int) -> bool:
    global PLAYERS, CURRENT_PLAYER

    player_pieces = PLAYERS[CURRENT_PLAYER]
    new_position = dice_number + position

    if new_position < START_POSITION or new_position > SAFE_END: 
        return False
    
    return all([p != new_position for p in player_pieces])

def get_selectable_pieces(dice_number: int) -> List[bool]:
    global CURRENT_PLAYER, PLAYERS

    selectable_pieces = []
    player_pieces = PLAYERS[CURRENT_PLAYER]

    for position in player_pieces:
        selectable_pieces.append(
           _is_piece_selectable(position, dice_number)
        )

    return selectable_pieces

# None means no peice took the position,
# and any other number means index of peice than took the position.
def _get_taken_piece_index(
    players, 
    current_player, 
    poistion, 
    other_player_number
) -> Optional[int]:
    
    relative_position = (poistion - (other_player_number - current_player) * 9) % 36
    other_player_pieces = players[other_player_number]

    index = 0 
    while index < len(other_player_pieces):
        piece_position = other_player_pieces[index]
        if piece_position == relative_position:
            return index
        index += 1 
    return None


def _is_taken_by_other_players(
        players, 
        current_player, 
        position
) -> Optional[Tuple[int, int]]: 
    
    for player in range(4): 
        if player == current_player:
            continue
        
        index = _get_taken_piece_index(
            players, current_player, position, player
        )
        if index is not None: 
            return (player, index)

def perform_move(dice_number, piece_number):
    global PLAYERS, CURRENT_PLAYER
    
    player_pieces = PLAYERS[CURRENT_PLAYER]
    position = player_pieces[piece_number]

    if not _is_piece_selectable(position, dice_number):
        raise InvalidMove()

    new_position = position + dice_number

    intersection = _is_taken_by_other_players(PLAYERS, CURRENT_PLAYER, new_position)
    if intersection is not None:
        taken_player, taken_index = intersection
        PLAYERS[taken_player][taken_index] = -6
    
    PLAYERS[CURRENT_PLAYER][piece_number] = new_position



def check_winner() -> Optional[int]:
    for player in range(4):
        all_home = all([
            SAFE_START <= p <= SAFE_END 
            for p in PLAYERS[player]
        ])
        if all_home:
            return player
        return None

