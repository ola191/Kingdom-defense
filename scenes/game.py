import json
import math
from collections import deque

import pygame
import sys

from Game.assets import get_texture
from Game.enemy import spawn_enemy, move_enemies
from Game.map import calculate_start_and_block_unit, load_map_data
from ui.colors import ui_color_black, ui_color_white, ui_color_red, ui_color_green, ui_color_sand, \
    ui_color_tower, ui_color_blue, ui_color_yellow, ui_color_grass_100
from ui.components.button import ui_button
from ui.filters.brightness import ui_brightness
from ui.layout.navbar import layout_navbar

fps = 0
clock = pygame.time.Clock()


class SceneGame:
    def __init__(self, screen, level_name):
        self.path = None
        self.startCord = (0,3)
        self.endCord = (29, 25)

        self.mapUnit = None

        self.cache = {}

        self.font =  pygame.font.Font(None,30)

        self.screen = screen
        self.level_name = level_name
        self.running = True
        self.map_data = load_map_data(self, level_name)
        self.config_data = self.load_json_data("data/config.json")
        self.draw_path()
        self.width, self.height = self.screen.get_size()

        self.map_unit = min(self.width / len(self.map_data[0]), self.height / len(self.map_data))

        self.brightness_from_config = self.config_data["settings"]["brightness"]

        self.filter = ui_brightness(screen, self.brightness_from_config)

        self.textures = {
            100 : get_texture("grass_01", (self.map_unit, self.map_unit)),
            101 : get_texture("grass_02",  (self.map_unit, self.map_unit)),
            102 : get_texture("grass_03",  (self.map_unit, self.map_unit)),
            200 : get_texture("path_01",  (self.map_unit, self.map_unit)),
            301 : get_texture("tower_01",  (self.map_unit, self.map_unit)),
            302 : get_texture("tower_02", (self.map_unit, self.map_unit)),
            303 : get_texture("tower_03", (self.map_unit, self.map_unit)),
            304 : get_texture("tower_04", (self.map_unit, self.map_unit)),
            305 : get_texture("tower_05", (self.map_unit, self.map_unit)),
            306 : get_texture("tower_06", (self.map_unit, self.map_unit)),
        }



        self.circles = []

        self.towers = []
        self.enemies = []
        self.gold = None
        self.enemies_types = []
        self.enemies_spawn_timer = None
        self.enemies_spawn_delay = None
        self.enemies_speed = None

        self.load_game_settings(self.level_name, self.config_data)

        self.money_button = ui_button(screen, f"{self.gold}", (0, 0), (75, 50),  None, "button_vertical.png", 100)
        self.navbar_buttons = [self.money_button]

        self.navbar_positions = layout_navbar(self.navbar_buttons, self.width, self.height, 10, "left", 25, 20)


    def load_json_data(self, filename):
        with open(filename, "r") as jsonFile:
            return json.load(jsonFile)

    def load_game_settings(self, level_name, config_data):
        game_settings_data = None

        for level in config_data["levels"]:
            if level["title"] == level_name:
                game_settings_data = level.get("settings")

        self.gold = game_settings_data["gold"]
        self.enemies_types = game_settings_data["enemies"]["types"]
        self.enemies_speed = game_settings_data["enemies"]["speed"]
        self.enemies_spawn_delay = game_settings_data["enemies"]["spawn_delay"]
        self.enemies_spawn_timer = game_settings_data["enemies"]["spawn_timer"]



    def draw_map(self):

        start_x, start_y, block_unit = calculate_start_and_block_unit(self)

        self.mapUnit = block_unit

        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                block_type = self.map_data[row][col]
                color = ui_color_red

                texture = self.textures.get(block_type)
                if texture: self.screen.blit(texture, (start_x + col * block_unit, start_y + row * block_unit))


    def draw_towers(self):
        for tower in self.towers:
            pass

    def draw_enemies(self):
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, ui_color_black, enemy["rect"])



    def find_path(self, start, goal):
        rows = len(self.map_data)
        cols = len(self.map_data[0])

        path = []
        directions = []

        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                if row % 2 == 0 and col % 2 == 0:
                    if self.map_data[row][col] == 200:
                        path.append((row, col))

        spacing_to_check = [(0,1), (0,-1), (1, 0), (-1, 0), (-1,-1), (1,1), (1,-1), (-1,1)]

        edges = set()

        for x, y in path:
            for direction in spacing_to_check:
                nr, nc = x + direction[0], y + direction[1]
                if 0 <= nr < rows and 0 <= nc < cols:
                    if self.map_data[nr][nc] == 100:
                        edges.add((x, y))
                        break

        for point in edges:
            if point in path:
                path.remove(point)

        for x, y in path:
            gravity_point = (x,y)
            points_within_distance = self.find_points_within_distance(path, x, y, 8)
            filtered_points, avg_direction = self.filter_points_by_direction(points_within_distance, gravity_point)
            to_remove = list(set(points_within_distance)&set(filtered_points))
            for point in to_remove:
                path.remove(point)

        return path

    def find_points_within_distance(self, path, x, y, max_distance):
        cache_key = (tuple(path), x, y, max_distance)

        if cache_key in self.cache:
            return self.cache[cache_key]

        nearby_points = []

        for pX, pY in path:
            # distance = math.sqrt((pX - x) ** 2 + (pY - y) ** 2)
            distance = abs(pX - x) + abs(pY - y)

            if distance <= max_distance:
                # if pX != x and pY != y:
                nearby_points.append((pX, pY))

        if (x,y) in nearby_points:
            nearby_points.remove((x, y))

        self.cache[cache_key] = nearby_points

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
        if not self.path:
            return

        reference_point = self.path[0]

        self.path.sort(key=lambda point: math.dist(reference_point, point))

    def update_gold(self, action):
        if self.gold > 999:
            self.money_button.rect.width = 100
        else:
            self.money_button.rect.width = 75

        actions = {
            "add" : 300,
            "tower" : -50,
        }

        if action in actions:
            self.gold += actions[action]

        self.money_button.text = f"{self.gold}"

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouuse_pos = pygame.mouse.get_pos()
                self.handle_click(mouuse_pos)

    def handle_click(self, mouse_pos):
        start_x, start_y, block_unit = calculate_start_and_block_unit(self)
        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                if self.map_data[row][col] == 300:
                    tower_rect = pygame.Rect(start_x + col * block_unit, start_y + row * block_unit, block_unit, block_unit)
                    if tower_rect.collidepoint(mouse_pos):
                        self.on_tower_click(row, col)

                square_size = block_unit / 3
                square_positions = [
                    (start_x + col * block_unit + (block_unit / 2) - (square_size / 2),
                     start_y + row * block_unit - square_size),
                    (start_x + col * block_unit + (block_unit / 2) + (square_size / 2),
                     start_y + row * block_unit - square_size),
                    (start_x + col * block_unit + (block_unit / 2) - (square_size / 2),
                     start_y + row * block_unit + (block_unit / 2)),
                    (start_x + col * block_unit + (block_unit / 2) + (square_size / 2),
                     start_y + row * block_unit + (block_unit / 2))
                ]

                for pos in square_positions:
                    square_rect = pygame.Rect(pos[0], pos[1], square_size, square_size)
                    if square_rect.collidepoint(mouse_pos):
                        self.handle_square_click(row, col)

    def handle_square_click(self, row, col):
        print(f"Square clicked for tower at ({row}, {col})")

    def on_tower_click(self, row, col):
        self.circles.append((row,col))
        # self.draw_circle_and_squares()

    def draw_circle_and_squares(self):
        for row,col in self.circles:
            start_x, start_y, block_unit = calculate_start_and_block_unit(self)
            center_x = start_x + col * block_unit + block_unit / 2
            center_y = start_y + row * block_unit + block_unit / 2
    
            radius = block_unit * 1.5
            pygame.draw.circle(self.screen, ui_color_black, (int(center_x), int(center_y)), int(radius), 1)
    
            colors = [ui_color_red, ui_color_green, ui_color_blue, ui_color_yellow]
            square_size = block_unit / 3
            square_positions = [
                (center_x - square_size, center_y - square_size),  # Top-left
                (center_x + square_size, center_y - square_size),  # Top-right
                (center_x - square_size, center_y + square_size),  # Bottom-left
                (center_x + square_size, center_y + square_size)   # Bottom-right
            ]
    
            for pos, color in zip(square_positions, colors):
                pygame.draw.rect(self.screen, color, (*pos, square_size, square_size))

    def draw(self):
        # self.screen.fill(ui_color_grass)
        self.screen.fill(ui_color_grass_100)
        self.draw_map()
        self.draw_towers()
        self.draw_enemies()
        
        self.draw_circle_and_squares()
        
        for button, (x,y) in zip(self.navbar_buttons, self.navbar_positions):
            button.position = (x, y)
            button.draw()

        self.filter.draw()
        text = self.font.render("Score:" + str(fps), 1, (0, 0, 0))
        self.screen.blit(text, (150, 20))
        pygame.display.flip()

    def update(self):
        self.enemies_spawn_timer += 1
        if self.enemies_spawn_timer >= self.enemies_spawn_delay:
            if len(self.enemies) < 10:
                spawn_enemy(self)
                self.enemies_spawn_timer = 0
        move_enemies(self)

def scene_game(screen, level_name):
    game_scene = SceneGame(screen, level_name)

    # print(', '.join("%s: %s" % item for item in vars(game_scene).items()))

    global fps
    while game_scene.running:
        pygame.event.pump()
        fps = clock.get_fps()
        clock.tick(60)
        for event in pygame.event.get():
            scene_action = game_scene.handle_event(event)
            if scene_action:
                return scene_action

        game_scene.update()
        game_scene.draw()

    pygame.quit()