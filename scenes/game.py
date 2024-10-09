import json

import pygame
import sys

from ui.colors import ui_color_black, ui_color_white, ui_color_red, ui_color_green, ui_color_sand, ui_color_grass
from ui.components.button import ui_button
from ui.filters.brightness import ui_brightness

class SceneGame:
    def __init__(self, screen, level_name):
        self.screen = screen
        self.level_name = level_name
        self.running = True
        self.map_data = self.load_map_data(level_name)
        self.width, self.height = self.screen.get_size()

        with open("data/config.json", "r") as mC:
            data = json.load(mC)
            self.brightness_from_config = data["settings"]["brightness"]

        self.filter = ui_brightness(screen, self.brightness_from_config)

    def load_map_data(self, level_name):
        # mC ~ mainConfig
        with open("data/config.json", "r") as mC:
            data = json.load(mC)
            for level in data["levels"]:
                if level["title"] == level_name:
                    return level.get("map")

    def calculate_start_and_block_unit(self):
        map_width = len(self.map_data[0])
        map_height = len(self.map_data)

        block_unit = min(self.width / map_width, self.height / map_height)

        start_x = (self.width - (block_unit * map_width)) / 2
        start_y = (self.height - (block_unit * map_height)) / 2

        return start_x, start_y, block_unit

    def draw_map(self):

        start_x, start_y, block_unit = self.calculate_start_and_block_unit()

        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                block_type = self.map_data[row][col]
                color = ui_color_red
                if block_type == 0:
                    color = ui_color_grass
                elif block_type == 1:
                    color = ui_color_sand
                pygame.draw.rect(self.screen, color,
                                 (start_x + col * block_unit, start_y + row * block_unit, block_unit, block_unit))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'levels'

    def draw(self):
        self.screen.fill(ui_color_grass)
        self.draw_map()
        self.filter.draw()
        pygame.display.flip()

def scene_game(screen, level_name):
    game_scene = SceneGame(screen, level_name)

    while game_scene.running:
        for event in pygame.event.get():
            scene_action = game_scene.handle_event(event)
            if scene_action:
                return scene_action

        game_scene.draw()

    pygame.quit()