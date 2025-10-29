import pygame

from .draw import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH
)

from .colors import (
    COLOR_BLACK
)

def draw_dice_number(screen, dice_number: int): 
    dice_x = SCREEN_WIDTH / 2 - 50  
    dice_y = SCREEN_HEIGHT / 2 - 50 

    cordinates = {
        1: [(50, 50)],
        2: [(30, 30), (70, 70)],
        3: [(30, 30), (50, 50), (70, 70)],
        4: [(30, 30), (70, 30), (30, 70), (70, 70)],
        5: [(30, 30), (70, 30), (50, 50), (30, 70), (70, 70)],
        6: [(30, 30), (70, 30), (30, 50), (70, 50), (30, 70), (70, 70)],
    }

    for cord in cordinates.get(dice_number, []):
        pygame.draw.circle(screen, COLOR_BLACK, (dice_x + cord[0], dice_y + cord[1]), 7)
        