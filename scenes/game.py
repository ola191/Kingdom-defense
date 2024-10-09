import json

import pygame
import sys

from ui.colors import ui_color_black, ui_color_white, ui_color_red, ui_color_green, ui_color_sand, ui_color_grass
from ui.components.button import ui_button

def calculate_start_and_block_unit(screen, map_data):
    width, height = screen.get_size()
    map_width = len(map_data[0])
    map_height = len(map_data)

    block_unit = min(width / map_width, height / map_height)

    start_x = (width - (block_unit * map_width)) / 2
    start_y = (height - (block_unit * map_height)) / 2

    return start_x, start_y, block_unit

def draw_map(screen, map_data):

    start_x, start_y, block_unit = calculate_start_and_block_unit(screen, map_data)

    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            block_type = map_data[row][col]
            color = ui_color_red
            if block_type == 0:
                color = ui_color_grass
            elif block_type == 1:
                color = ui_color_sand
            pygame.draw.rect(screen, color, (start_x + col * block_unit ,start_y + row * block_unit, block_unit, block_unit))

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
        screen.fill(ui_color_grass)

        draw_map(screen, map_data)

        # title_button = ui_button(screen, f"{level_name}", (300, 100), (200,50))
        # back_button = ui_button(screen, "back to main menu", (300, 200), (200, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if back_button.collidepoint(event.pos):
            #         return 'main_menu'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'levels'

    pygame.quit()