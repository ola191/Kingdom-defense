from pydoc_data.topics import topics

import pygame
import sys

from ui.components.button import ui_button
from ui.layout.column import layout_column


def start_game(screen):
    pass

def open_settings(screen):
    pass

def quit_game():
    pygame.quit()
    sys.exit()

def scene_main_menu(screen):
    running = True
    while running:
        screen.fill((0, 0, 0))

        start_button = ui_button(screen, "Start Game", (0, 0), (300, 50))
        settings_button = ui_button(screen, "Settings", (0, 0), (300, 50))
        quit_button = ui_button(screen, "Close Game", (0, 0), (300, 50))

        buttons_to_layout = [start_button, settings_button, quit_button]
        spacing = 20
        available_width, available_height = screen.get_size()
        positions = layout_column(buttons_to_layout, available_width, available_height, spacing)

        for button, (x,y) in zip(buttons_to_layout, positions):
            button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    print("1")
                    return 'levels'
                elif settings_button.collidepoint(event.pos):
                    print("2")
                    return 'settings'
                elif quit_button.collidepoint(event.pos):
                    print("4")
                    quit_game()

    pygame.quit()
