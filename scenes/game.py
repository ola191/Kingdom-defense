import json

import pygame
import sys

from ui.components.button import ui_button

def scene_game(screen, level_name):
    running = True

    # with
    while running:
        screen.fill((0, 0, 0))

        title_button = ui_button(screen, f"{level_name}", (300, 100), (200,50))
        back_button = ui_button(screen, "back to main menu", (300, 200), (200, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return 'main_menu'

    pygame.quit()