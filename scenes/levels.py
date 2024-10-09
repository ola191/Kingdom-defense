import json

import pygame
import sys

from ui.components.button import ui_button

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

        actual_y = 100

        for level in levels:
            button_rect = ui_button(screen, level, (300, actual_y), (200, 50))
            levels_buttons.append((button_rect, level))
            actual_y += 70

        back_button = ui_button(screen, "back to main menu", (300, actual_y), (200, 50))

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