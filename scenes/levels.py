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
        print(data)
        for level in data["levels"]:
            levels.append(level['title'])

    while running:
        screen.fill((0, 0, 0))

        actual_y = 100

        for level in levels:
            ui_button(screen, level, (300, actual_y), (200, 50))
            actual_y += 70

        back_button = ui_button(screen, "back to main menu", (300, actual_y), (200, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return 'main_menu'

    pygame.quit()