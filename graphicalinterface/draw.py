from typing import Tuple, List

import pygame


SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

CIRCLE_RADIUS = 25
GRID_SIZE = 11
CELL_SIZE = 62.5
GRID_START_X = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) # => 62.5
GRID_START_Y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) 


def get_position_coordinates(position: Tuple[int, int]): 
    return (GRID_START_X + position[0] * CELL_SIZE, 
            GRID_START_Y + position[1] * CELL_SIZE)



def draw_cells(screen: pygame.Surface,
               cells: List[List[Tuple]],
               color_mapping
               ): 
    
    for player, poses in enumerate(cells):
        for pos in poses:
            pygame.draw.circle(
                screen, 
                color_mapping[player],
                get_position_coordinates(pos),
                CIRCLE_RADIUS
            )

def draw_single_peice(screen, pos: Tuple[int, int], piece_number: int, color): 
    font = pygame.font.SysFont("Arial", 30)
    text_surface = font.render(str(piece_number + 1), True, color) # draw text
    text_rect = text_surface.get_rect(center = get_position_coordinates(pos)) #  text_position
    screen.blit(text_surface, text_rect)



    

