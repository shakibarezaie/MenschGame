from typing import List, Tuple

from collections import defaultdict

import pygame

import itertools

import core.board as board

from core.board import (
    SAFE_START,
    SAFE_END,
)

from .colors import (
    COLOR_WHITE,
    COLOR_BEIGE,
    COLOR_BLACK,
    COLOR_GRAY,
    COLOR_RED,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_YELLOW,
)

from .state import (
    WAITING_FOR_DICE_ROLL,
    WAITING_FOR_SELECT_PIECE
)



from .positions import (
    get_home_positions,
    get_starting_positions,
    get_safe_postions,
    get_white_cells_postions,
    get_position,
    COLOR_MAPPING,
    LIGHT_COLOR_MAPPING
)

from .draw import (
    draw_cells, 
    draw_single_peice,
    SCREEN_HEIGHT,
    SCREEN_WIDTH 
)

from .dice import draw_dice_number




KEYS_MAPPING = {
    pygame.K_1: 0,
    pygame.K_2: 1, 
    pygame.K_3: 2,
    pygame.K_4: 3
}

FONT_PATH = "/Users/shakiba/Desktop/university/project/assets/SuperMario256.ttf" 
DICE_SOUND_PATH = "/Users/shakiba/Desktop/university/project/assets/dicerolling.mp3"


def init_screen() -> Tuple[pygame.Surface, pygame.time.Clock]:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mensch")
    clock = pygame.time.Clock()
    return screen, clock




def how_to_play_screen():
    screen, clock = init_screen()

    font1 = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)

    text1 = font1.render("How to Play:", True, (0, 0, 0))
    text2 = font2.render("- roll the six-sided die on your turn to determine your move.", True, (0, 0, 0))
    text3 = font2.render("- roll a 6 to move a piece out of your 'home' area onto the board.", True, (0, 0, 0))
    text4 = font2.render("- rolling a 6 also gives you another turn.", True, (0, 0, 0))
    text5 = font2.render("- landing on an opponent's piece sends it back to their starting area.", True, (0, 0, 0))
    text6 = font2.render("- move all your pieces in to your safe zone to win.", True, (0, 0, 0))
    text7 = font2.render("press 'left arrow' to return to the menu.", True, (0, 0, 0))
    extra_line = font1.render("", True, (0, 0, 0))

    running = True
    while running:
        screen.fill(COLOR_WHITE)

        screen.blit(text1, (100, 200))
        screen.blit(extra_line, (100, 250))
        screen.blit(text2, (100, 280))
        screen.blit(text3, (100, 310))
        screen.blit(text4, (100, 340))
        screen.blit(text5, (100, 370))
        screen.blit(text6, (100, 400))
        screen.blit(extra_line, (100, 430))
        screen.blit(text7, (100, 480))
        

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        running = False

        pygame.display.flip()
        clock.tick(60)



def color_cycler(colors: List):
    return itertools.cycle(colors)



def screen():
    screen, clock = init_screen()
    colors = [COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW]
    font = pygame.font.Font(FONT_PATH, 100)
    text = "MENSCH"
    color_cycle = color_cycler(colors)
    current_color = next(color_cycle)
    color_change_delay = 500 
    last_color_change = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: 
                    running = False

        now = pygame.time.get_ticks()
        if now - last_color_change > color_change_delay:
            current_color = next(color_cycle)
            last_color_change = now

        screen.fill(COLOR_WHITE)
        text_surface = font.render(text, True, current_color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(60)

    menu()



def menu():
    menu_options = ["New Game", "How to Play", "Exit"]
    selected_option = 0
    screen, clock = init_screen()
    font = pygame.font.Font(None, 50)

    option_height = 50
    total_height = len(menu_options) * option_height
    start_y = (SCREEN_HEIGHT - total_height) // 2

    while True:
        screen.fill(COLOR_WHITE)

        for i, option in enumerate(menu_options):
            if i == selected_option:
                color = COLOR_GREEN
            else:
                color = COLOR_BLACK

            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * option_height))
            screen.blit(text_surface, text_rect)

         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 3
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0: 
                        start_game()
                    elif selected_option == 1:
                        how_to_play_screen()
                    elif selected_option == 2: 
                        pygame.quit()
                        raise SystemExit

        pygame.display.flip()
        clock.tick(60)


def start_game():
    screen, clock = init_screen()
    dice_number = None 
    state = WAITING_FOR_DICE_ROLL
    players_state = board.get_players_state()
    current_player = board.get_current_player()

    
    while True:
        state, dice_number = handle_game_action(state, dice_number)
        players_state = board.get_players_state()
        current_player = board.get_current_player()

        
        winner = board.check_winner()
        if winner is not None:
            show_winner(winner)
            break

        if (state == WAITING_FOR_SELECT_PIECE and 
            not any(board.get_selectable_pieces(dice_number))):
            board.next_turn(dice_number)
            state = WAITING_FOR_DICE_ROLL

        draw_board(screen)
        show_players_state(screen, players_state)
        
        if dice_number is not None:
            draw_dice_number(screen, dice_number)
        
        if state == WAITING_FOR_SELECT_PIECE:
            show_unselectable_pieces(
                screen,
                current_player,
                players_state, 
                board.get_selectable_pieces(dice_number)
            )
        show_turn_indicator(screen, current_player)
        pygame.display.flip()
        clock.tick(60)  


def handle_game_action(state, dice_number):
    dice_sound = pygame.mixer.Sound(DICE_SOUND_PATH) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        if event.type != pygame.KEYDOWN:
            continue

        if (state == WAITING_FOR_DICE_ROLL and 
            event.key == pygame.K_SPACE):
            dice_sound.play()
            return WAITING_FOR_SELECT_PIECE, board.roll_dice()
        

        
        if (state == WAITING_FOR_SELECT_PIECE and 
            event.key in KEYS_MAPPING.keys()):
            try:
                board.perform_move(dice_number, KEYS_MAPPING[event.key])
            except board.InvalidMove:
                print("invalid move.")
                continue
            board.next_turn(dice_number)
            return WAITING_FOR_DICE_ROLL, dice_number
        
    return state, dice_number


def show_home_cells(screen: pygame.Surface):
    home_coordinates = get_home_positions()
    draw_cells(screen, home_coordinates, COLOR_MAPPING)



def show_starting_cells(screen: pygame.Surface):
    starting_postions = get_starting_positions()
    draw_cells(screen, starting_postions, LIGHT_COLOR_MAPPING)



def show_safe_cells(screen: pygame.Surface):
    final_positions = get_safe_postions()
    draw_cells(screen, final_positions, COLOR_MAPPING)



def show_white_cells(screen: pygame.Surface):
    default_cells = get_white_cells_postions()
    draw_cells(screen, default_cells, defaultdict(lambda: COLOR_WHITE))



def draw_board(screen: pygame.Surface):
    screen.fill(COLOR_BEIGE)
    show_white_cells(screen)
    show_home_cells(screen)
    show_starting_cells(screen)
    show_safe_cells(screen)



def show_players_state(screen, players_state: List[List[int]]):
    for player_number, player_state in enumerate(players_state):
        for piece_number, piece in enumerate(player_state): 
            if piece == -6 or SAFE_START <= piece <= SAFE_END:
                color = COLOR_BLACK
            
            else:
                color = COLOR_MAPPING[player_number]

            draw_single_peice(
                screen=screen, 
                pos=get_position(player_number, piece_number, piece), 
                piece_number=piece_number, 
                color=color,
            )

def show_unselectable_pieces(
        screen, 
        current_player: int, 
        players_state: List[List[int]], 
        selectable_pieces: List[bool]
):
    player_state = players_state[current_player]
    for piece_number, piece in enumerate(player_state): 
        if selectable_pieces[piece_number]: 
            continue

        draw_single_peice(
            screen=screen, 
            pos=get_position(current_player, piece_number, piece), 
            piece_number=piece_number, 
            color=COLOR_GRAY,
        )



def show_turn_indicator(screen, current_player):
    font = pygame.font.SysFont('Arial', 20)  
    player_colors = ["Red", "Blue", "Green", "Yellow"]
    text = f"Turn: {player_colors[current_player]}"
    text_surface = font.render(text, True, COLOR_MAPPING[current_player])

    screen.blit(text_surface, (10, 10)) 

def show_winner(winner_player_number):
    pass 
