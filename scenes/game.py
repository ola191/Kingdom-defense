import json

import pygame
import sys

from ui.colors import ui_color_black, ui_color_white, ui_color_red, ui_color_green, ui_color_sand, ui_color_grass
from ui.components.button import ui_button

def draw_map(screen, map_data):

    width, height = screen.get_size()

    block_unit = width / (len(map_data[0]))
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            block_type = map_data[row][col]
            color = ui_color_red
            if block_type == 0:
                color = ui_color_grass
            elif block_type == 1:
                color = ui_color_sand
            pygame.draw.rect(screen, color, (col * block_unit , row * block_unit, block_unit, block_unit))

def load_map_data(level_name):
    # mC ~ mainConfig
    with open("data/config.json", "r") as mC:
        data = json.load(mC)
        for level in data["levels"]:
            if level["title"] == level_name:
                return level.get("map")

def scene_game(screen, level_name):
    running = True

    map_data = load_map_data(level_name)


    while running:
        screen.fill((0, 0, 0))

        draw_map(screen, map_data)

        # title_button = ui_button(screen, f"{level_name}", (300, 100), (200,50))
        # back_button = ui_button(screen, "back to main menu", (300, 200), (200, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return 'main_menu'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'levels'

    pygame.quit()