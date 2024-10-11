import json
import math
from collections import deque

import pygame
import sys

from ui.colors import ui_color_black, ui_color_white, ui_color_red, ui_color_green, ui_color_sand, ui_color_grass, \
    ui_color_tower
from ui.components.button import ui_button
from ui.filters.brightness import ui_brightness

class SceneGame:
    def __init__(self, screen, level_name):

        self.path = None
        self.startCord = (0,3)
        self.endCord = (29, 25)

        self.mapUnit = None

        self.screen = screen
        self.level_name = level_name
        self.running = True
        self.map_data = self.load_map_data(level_name)
        self.draw_path()
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

        self.mapUnit = block_unit

        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                block_type = self.map_data[row][col]
                color = ui_color_red
                if block_type == 0:
                    color = ui_color_grass
                elif block_type == 1:
                    color = ui_color_sand
                elif block_type == 2:
                    color = ui_color_tower
                elif block_type == 3:
                    color = ui_color_red
                pygame.draw.rect(self.screen, color,
                                 (start_x + col * block_unit, start_y + row * block_unit, block_unit, block_unit))

    def draw_towers(self):
        for tower in self.towers:
            pass

    def draw_enemies(self):
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, ui_color_black, enemy["rect"])

    def spawn_enemy(self):
        mapUnit = self.mapUnit

        x, y = (self.startCord[1]) * mapUnit, self.startCord[0] * mapUnit
        enemy = {
            "rect": pygame.Rect(x, y, mapUnit, mapUnit),
            "path_index": 0
        }
        self.enemies.append(enemy)

    def move_enemies(self):
        mapUnit = self.mapUnit
        enemies_to_remove = []

        for enemy in self.enemies:
            current_index = enemy["path_index"]

            if current_index < len(self.path) - 1:
                next_point = self.path[current_index + 1]
                enemy_rect = enemy["rect"]

                target_x = next_point[1] * mapUnit
                target_y = next_point[0] * mapUnit

                dx = target_x - enemy_rect.x
                dy = target_y - enemy_rect.y

                dist = math.sqrt(dx ** 2 + dy ** 2)

                if dist != 0:
                    move_x = self.enemies_speed * (dx / dist)
                    move_y = self.enemies_speed * (dy / dist)
                else:
                    move_x, move_y = 0, 0

                enemy_rect.x += move_x
                enemy_rect.y += move_y

                if abs(enemy_rect.x - target_x) < self.enemies_speed and abs(
                        enemy_rect.y - target_y) < self.enemies_speed:
                    enemy["path_index"] += 1
            else:
                enemies_to_remove.append(enemy)
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

    def find_path(self, start, goal):
        rows = len(self.map_data)
        cols = len(self.map_data[0])

        path = []
        directions = []

        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                if row % 2 == 0 and col % 2 == 0:
                    if self.map_data[row][col] == 1:
                        path.append((row, col))

        spacing_to_check = [(0,1), (0,-1), (1, 0), (-1, 0), (-1,-1), (1,1), (1,-1), (-1,1)]

        edges = []

        for x, y in path:
            for direction in spacing_to_check:
                nr, nc = x + direction[0], y + direction[1]
                if 0 <= nr < rows and 0 <= nc < cols:
                    if self.map_data[nr][nc] == 0:
                        edges.append((x, y))
                        break

        for point in edges:
            if point in path:
                path.remove(point)

        for x, y in path:
            gravity_point = (x,y)
            points_within_distance = self.find_points_within_distance(path, x, y, 8)
            filtered_points, avg_direction = self.filter_points_by_direction(points_within_distance, gravity_point)
            print(filtered_points, avg_direction)
            to_remove = list(set(points_within_distance)&set(filtered_points))
            for point in to_remove:
                path.remove(point)

        return path

    def find_points_within_distance(self, path, x, y, max_distance):
        nearby_points = []

        for pX, pY in path:
            # distance = math.sqrt((pX - x) ** 2 + (pY - y) ** 2)
            distance = abs(pX - x) + abs(pY - y)

            if distance <= max_distance:
                # if pX != x and pY != y:
                nearby_points.append((pX, pY))

        if (x,y) in nearby_points:
            nearby_points.remove((x, y))

        return nearby_points

    def calculate_angle(self, p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        angle = math.degrees(math.atan2(dy, dx))
        return angle if angle >= 0 else 360 + angle

    def classify_angle(self, angle):
        directions = [0, 45, 90, 135, 180, 225, 270, 315]
        closest_direction = min(directions, key=lambda x: abs(x - angle))
        return closest_direction

    def average_direction(self, angles):
        x = sum(math.cos(math.radians(angle)) for angle in angles) / len(angles)
        y = sum(math.sin(math.radians(angle)) for angle in angles) / len(angles)
        avg_angle = math.degrees(math.atan2(y, x))
        return avg_angle if avg_angle >= 0 else 360 + avg_angle

    def filter_points_by_direction(self, points, main_point):
        angles = [self.calculate_angle(main_point, p) for p in points]
        classified_angles = [self.classify_angle(angle) for angle in angles]
        avg_angle = self.classify_angle(self.average_direction(classified_angles))

        filtered_points = [p for p, angle in zip(points, classified_angles) if angle == avg_angle]

        return filtered_points, avg_angle

    def sort_path_by_distance(self):
        sorted_path = [self.path[0]]
        remaining_points = self.path[1:]

        while remaining_points:
            last_point = sorted_path[-1]
            nearest_point = min(remaining_points, key=lambda point: math.dist(last_point, point))
            sorted_path.append(nearest_point)
            remaining_points.remove(nearest_point)

        self.path = sorted_path

    def draw_path(self):

        self.path = self.find_path(self.startCord, self.endCord)
        self.sort_path_by_distance()
        # if self.path is not None:
        #     for x, y in self.path:
        #         self.map_data[x][y] = 2

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'levels'

    def draw(self):
        # self.screen.fill(ui_color_grass)
        self.screen.fill(ui_color_red)
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