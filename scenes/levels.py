import json

import pygame
import sys

from ui.components.button import ui_button
from ui.layout.column import layout_column


def scene_levels(screen):
    running = True

    levels = []

    # mC ~ mainConfig
    with open("data/config.json", "r") as mC:
        data = json.load(mC)
        for level in data["levels"]:
            levels.append(level['title'])

    levels_buttons = []

    while running:
        screen.fill((0, 0, 0))

        buttons_to_layout = []

        for level in levels:
            button_rect = ui_button(screen, level, (0, 0), (300, 50))
            levels_buttons.append((button_rect, level))
            buttons_to_layout.append(button_rect)

        back_button = ui_button(screen, "back to main menu", (0, 0), (300, 50))

        buttons_to_layout.append(back_button)

        spacing = 20
        available_width, available_height = screen.get_size()
        positions = layout_column(buttons_to_layout, available_width, available_height, spacing)

        for button, (x, y) in zip(buttons_to_layout, positions):
            button.position = (x, y)
            button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return 'main_menu'
                for button_rect, level in levels_buttons:
                    if button_rect.collidepoint(event.pos):
                        return f'game_{level}'

    pygame.quit()