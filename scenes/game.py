import json
from collections import deque

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

        self.towers = []
        self.enemies = []
        self.gold = None
        self.enemies_types = []
        self.enemies_spawn_timer = None
        self.enemies_spawn_delay = None
        self.enemies_speed = None

        self.load_game_settings(self.level_name)

    def load_map_data(self, level_name):
        # mC ~ mainConfig
        with open("data/config.json", "r") as mC:
            data = json.load(mC)
            for level in data["levels"]:
                if level["title"] == level_name:
                    return level.get("map")

    def load_game_settings(self, level_name):
        with open("data/config.json", "r") as mC:
            data = json.load(mC)

            game_settings_data = None

            for level in data["levels"]:
                if level["title"] == level_name:
                    game_settings_data = level.get("settings")

        self.gold = game_settings_data["gold"]
        self.enemies_types = game_settings_data["enemies"]["types"]
        self.enemies_speed = game_settings_data["enemies"]["speed"]
        self.enemies_spawn_delay = game_settings_data["enemies"]["spawn_delay"]
        self.enemies_spawn_timer = game_settings_data["enemies"]["spawn_timer"]

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

    def draw_towers(self):
        for tower in self.towers:
            pass

    def draw_enemies(self):
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, ui_color_black, enemy)

    def spawn_enemy(self):
        enemy = pygame.Rect(0,0, 50, 50)
        self.enemies.append(enemy)

        path = self.find_path((0,3), (27,9))
        print(f"path {path}")

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.x += self.enemies_speed

    def find_path(self, start, goal):
        rows, cols = len(self.map_data), len(self.map_data[0])

        if self.map_data[start[0]][start[1]] != 1 or self.map_data[goal[0]][goal[1]] != 1:
            return None

        visited = set()
        queue = deque([(start, [start])])

        iteration_limit = rows * cols

        while queue and iteration_limit > 0:
            (current_x, current_y), path = queue.popleft()

            if (current_x, current_y) == goal:
                return path

            visited.add((current_x, current_y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current_x + dx, current_y + dy)

                if (0 <= neighbor[0] < rows and
                        0 <= neighbor[1] < cols and
                        neighbor not in visited and
                        self.map_data[neighbor[0]][neighbor[1]] == 1):
                    queue.append((neighbor, path + [neighbor]))

            iteration_limit -= 1  # Zmniejsz licznik iteracji

        print(f"visited {visited}")
        print(f"queue {queue}")

        return None

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'levels'

    def draw(self):
        self.screen.fill(ui_color_grass)
        self.draw_map()
        self.draw_towers()
        self.draw_enemies()
        self.filter.draw()
        pygame.display.flip()

    def update(self):
        self.enemies_spawn_timer += 1
        if self.enemies_spawn_timer >= self.enemies_spawn_delay:
            if len(self.enemies) < 10:
                self.spawn_enemy()
                self.enemies_spawn_timer = 0
        self.move_enemies()

def scene_game(screen, level_name):
    game_scene = SceneGame(screen, level_name)

    # print(', '.join("%s: %s" % item for item in vars(game_scene).items()))

    while game_scene.running:
        for event in pygame.event.get():
            scene_action = game_scene.handle_event(event)
            if scene_action:
                return scene_action

        game_scene.update()
        game_scene.draw()

    pygame.quit()