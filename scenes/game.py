import json
import math
import time
from collections import deque
from functools import wraps, lru_cache

import pygame
import sys

from Game.Spirits.Tower import Tower
from Game.animations import load_animation
from Game.assets import get_texture
from Game.enemy import spawn_enemy
from Game.map import calculate_start_and_block_unit, load_map_data
from ui.animations import Animation
from ui.colors import ui_color_black, ui_color_white, ui_color_red, ui_color_green, ui_color_sand, \
    ui_color_tower, ui_color_blue, ui_color_yellow, ui_color_grass_100
from ui.components.button import ui_button
from ui.filters.brightness import ui_brightness
from ui.layout.column import layout_column
from ui.layout.navbar import layout_navbar
from ui.navigators.button_navigator import Navigator

fps = 0
clock = pygame.time.Clock()

def timing_decorator(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # {func.__name__}
        # {args}
        # {kwargs}
        print(f'Function Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper

class SceneGame:
    def __init__(self, screen, level_name):

        self.selected_tower_position = None
        self.path = None
        self.startCord = (0,3)
        self.endCord = (29, 25)

        self.mapUnit = None

        self.hearts = 5

        self.cache = {}
        self.angle_cache = {}

        self.help_counter = 0

        self.font =  pygame.font.Font(None,30)


        self.average = [0]
        self.screen = screen
        self.level_name = level_name
        self.running = True
        self.map_data = load_map_data(self, level_name)
        self.config_data = self.load_json_data("data/config.json")
        self.draw_path()
        self.width, self.height = self.screen.get_size()

        self.start_x, self.start_y, self.block_unit = calculate_start_and_block_unit(self)

        self.panel_visible = False

        self.panel_rect = pygame.Rect(self.width - 200, 50, 180, self.height - 100)
        self.background_image = pygame.transform.scale(pygame.image.load("images/ui/button_vertical.png"), (self.panel_rect.width, 50))

        self.brightness_from_config = self.config_data["settings"]["brightness"]

        self.filter = ui_brightness(screen, self.brightness_from_config)

        size = (self.block_unit, self.block_unit)
        self.textures = {
            100 : get_texture("grass_01", size),
            101 : get_texture("grass_02",  size),
            102 : get_texture("grass_03",  size),
            200 : get_texture("path_01",  size),
            301 : get_texture("tower_01",  size),
            302 : get_texture("tower_02", size),
            303 : get_texture("tower_03", size),
            304 : get_texture("tower_04", size),
            305 : get_texture("tower_05", size),
            306 : get_texture("tower_06", size),
            311 : get_texture("tower_archer_01", size),
            312 : get_texture("tower_archer_02", size),
            313 : get_texture("tower_archer_03", size),
            314 : get_texture("tower_archer_04", size),
            315 : get_texture("tower_archer_05", size),
            316 : get_texture("tower_archer_06", size),
            321: get_texture("tower_archer_01", size),
            322: get_texture("tower_archer_02", size),
            323: get_texture("tower_archer_03", size),
            324: get_texture("tower_archer_04", size),
            325: get_texture("tower_archer_05", size),
            326: get_texture("tower_archer_06", size),
        }

        self.animation_frames = load_animation("goblin", self.block_unit)

        self.freeze = False

        self.circles = []

        self.towers = []
        self.enemies = []
        self.gold = None
        self.enemies_number = None
        self.enemies_count = 0
        self.enemies_spawn_timer = None
        self.enemies_spawn_delay = None
        self.enemies_speed = None

        self.load_game_settings(self.level_name, self.config_data)

        self.money_button = ui_button(screen, f"{self.gold}", (0, 0), (75, 50),  None, "button_vertical.png", 100)
        self.hearts_button = ui_button(screen, f"{self.hearts}", (0,0), (75, 50), None, "button_vertical.png", 100)

        self.navbar_buttons = [self.money_button, self.hearts_button]

        self.navbar_positions = layout_navbar(self.navbar_buttons, self.width, self.height, 10, "left", 25, 20)


        self.end_menu_score_button = ui_button(self.screen, "Congratulations", (0,0), (300, 50), None, "button_vertical.png", 100)
        self.end_menu_gold_button = ui_button(self.screen, f"{self.gold}", (0,0), (50, 50), None, "button_vertical.png", 100)
        self.end_menu_return_to_levels = ui_button(self.screen, "Return", (0,0), (150, 50), None, "button_vertical.png", 100)

        self.end_menu_buttons = [
            self.end_menu_score_button, self.end_menu_gold_button, self.end_menu_return_to_levels
        ]

        self.end_menu_buttons[0].change_brightness(80)

        self.end_menu_buttons_positions = layout_column(self.end_menu_buttons, self.width, self.height, 10)

        self.button_navigator = Navigator(self.end_menu_buttons)

        self.selected_button = self.end_menu_buttons[0]

        self.button_navigator.update_selection()

        self.mixer = pygame.mixer
        self.mixer.init()

        self.click_sound = self.mixer.Sound("sounds/button_click.wav")

    def load_json_data(self, filename):
        with open(filename, "r") as jsonFile:
            return json.load(jsonFile)

    def load_game_settings(self, level_name, config_data):
        level_settings = next((level.get("settings") for level in config_data["levels"] if level["title"] == level_name), None)
        if level_settings:
            self.gold = level_settings["gold"]
            self.enemies_number = level_settings["enemies"]["types&info"]["goblin"]
            self.enemies_speed = level_settings["enemies"]["speed"]
            self.enemies_spawn_delay = level_settings["enemies"]["spawn_delay"]
            self.enemies_spawn_timer = level_settings["enemies"]["spawn_timer"]



    def draw_map(self):

        rows, cols = len(self.map_data), len(self.map_data[0])

        start_x, start_y, block_unit = self.start_x, self.start_y, self.block_unit

        map_data = self.map_data
        textures = self.textures

        for row in range(rows):
            for col in range(cols):
                block_type = map_data[row][col]

                texture = textures.get(block_type)
                if texture: self.screen.blit(texture, (start_x + col * block_unit, start_y + row * block_unit))


    def draw_towers(self):
        for tower in self.towers:
            texture = self.textures.get(321)
            if texture:
                x, y = tower.position
                self.screen.blit(texture, (x, y))

    def draw_enemies(self):
        # goblin_image = pygame.image.load("images/monsters/goblin.jpg")
        # goblin_image = pygame.transform.scale(goblin_image, (self.block_unit, self.block_unit))
        for enemy in self.enemies:
            # if enemy.alive:
            #     x,y = enemy.position
            #     self.screen.blit(goblin_image, (x, y))
            enemy.draw(self.screen)

    def find_path(self, start, goal):
        rows = len(self.map_data)
        cols = len(self.map_data[0])

        map_data = self.map_data

        path = [(row, col) for row in range(rows) for col in range(cols) if row % 2 == 0 and col % 2 == 0 and map_data[row][col] == 200]
        # path = []
        # for row in range(rows):
        #     for col in range(cols):
        #         if row % 2 == 0 and col % 2 == 0:
        #             if self.map_data[row][col] == 200:
        #                 path.append((row, col))

        spacing_to_check = [(0,1), (0,-1), (1, 0), (-1, 0), (-1,-1), (1,1), (1,-1), (-1,1)]
        # edges = set()
        edges = {(x,y) for x,y in path if any(0 <= x + dx < rows and 0 <= y + dy < cols and map_data[x + dx][y + dy] == 100 for dx, dy in spacing_to_check)}

        # for x, y in path:
        #     for direction in spacing_to_check:
        #         nr, nc = x + direction[0], y + direction[1]
        #         if 0 <= nr < rows and 0 <= nc < cols:
        #             if self.map_data[nr][nc] == 100:
        #                 edges.add((x, y))
        #                 break

        # path = [point for point in path if point not in edges]

        for point in edges:
            if point in path:
                path.remove(point)

        for x, y in path:
            points_within_distance = self.find_points_within_distance(path, x, y, 8)
            filtered_points, _ = self.filter_points_by_direction(points_within_distance, (x,y))
            # path = [point for point in path if point not in filtered_points]
            to_remove = list(set(points_within_distance)&set(filtered_points))
            for point in to_remove:
                path.remove(point)

        hardPath = [(0, 2), (3, 3), (6, 4), (9, 6), (10, 9), (11, 13), (12, 17), (11, 20), (10, 22), (9, 24), (8, 27), (8, 32), (9, 34), (12, 36), (15, 37), (18, 37), (20, 36), (22, 34), (24, 31), (25, 28), (27, 26), (29, 24)]

        for x, y in hardPath:
            self.map_data[x][y] = 321


        return hardPath

    def find_points_within_distance(self, path, x, y, max_distance):
        cache_key = (tuple(path), x, y, max_distance)

        if cache_key in self.cache:
            return self.cache[cache_key]

        nearby_points = [
            (pX, pY) for pX, pY in path
            if abs(pX - x) + abs(pY - y) <= max_distance
        ]

        nearby_points = [point for point in nearby_points if point != (x, y)]
        self.cache[cache_key] = nearby_points
        return nearby_points

    def calculate_angle(self, p1, p2):
        key = (p1, p2)
        if key in self.angle_cache:
            return self.angle_cache[key]

        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        angle = math.degrees(math.atan2(dy, dx)) % 360
        self.angle_cache[key] = angle
        return angle

    def classify_angle(self, angle):
        directions = [0, 45, 90, 135, 180, 225, 270, 315]
        closest_direction = min(directions, key=lambda x: abs(x - angle))
        return closest_direction

    def average_direction(self, angles):
        if not angles:
            return 0
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

    def update_gold(self, reward):
        if self.gold > 999:
            self.money_button.rect.width = 100
        else:
            self.money_button.rect.width = 75
        #
        # actions = {
        #     "add" : 300,
        #     "tower" : -50,
        # }
        #
        # if action in actions:
        #     self.gold += actions[action]

        self.gold += reward

        self.money_button.text = f"{self.gold}"

    def update_hearts(self, hearts):
        self.hearts += hearts

        self.hearts_button.text = f"{self.hearts} ❤️"

    def draw_path(self):

        self.path = self.find_path(self.startCord, self.endCord)
        # self.sort_path_by_distance()
        # if self.path is not None:
        #     for x, y in self.path:
        #         self.map_data[x][y] = 2

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'levels'
            elif event.key == pygame.K_DOWN:
                self.click_sound.play()

                self.button_navigator.next()
                self.selected_button = self.button_navigator.get_current()
            elif event.key == pygame.K_UP:
                self.click_sound.play()

                self.button_navigator.previous()
                self.selected_button = self.button_navigator.get_current()
            elif event.key == pygame.K_RETURN:

                current_button = self.button_navigator.get_current()
                if current_button == self.end_menu_return_to_levels:
                    self.click_sound.play()
                    return 'levels'
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button, level in zip(self.end_menu_buttons, self.end_menu_buttons_positions):
                if button.collidepoint(event.pos):
                    if button == self.end_menu_return_to_levels:
                        Animation.click_background(self.screen, 80, 40, 30, button, 200)
                        return("levels")
            self.handle_click(pygame.mouse.get_pos())



    def is_enemy_in_range(self, tower_position, enemy_position, range_limit=7):
        distance = math.sqrt((tower_position[0] - enemy_position[0]) ** 2 +
                             (tower_position[1] - enemy_position[1]) ** 2)
        return distance <= range_limit

    # def destroy_enemies_in_range(self):
    #     for tower in self.towers:
    #
    #         tower_position = (tower["rect"].x // self.block_unit, tower["rect"].y // self.block_unit)
    #         enemies_to_remove = []
    #         for enemy in self.enemies:
    #             enemy_position = (enemy["rect"].x // self.block_unit, enemy["rect"].y // self.block_unit)
    #
    #             if self.is_enemy_in_range(tower_position, enemy_position):
    #                 print(f"enemy at {enemy_position}")
    #                 enemies_to_remove.append(enemy)
    #
    #         for enemy in enemies_to_remove:
    #             self.enemies.remove(enemy)

    def update_enemies(self):
        if len(self.enemies) != 0:
            for enemy in self.enemies:
                if enemy.alive:
                    passed = enemy.move_enemy(self)
                    if passed:
                        self.update_hearts(passed)
        else:
            if self.enemies_count == self.enemies_number:
                self.freeze = True
                self.draw_end_menu()

    def update_towers(self):
        for tower in self.towers:
            pass
            # tower.attack(self.enemies)

    def handle_click(self, mouse_pos):


        if self.panel_rect.collidepoint(mouse_pos):
            archer_button_rect = pygame.Rect(self.panel_rect.x, self.panel_rect.y, self.panel_rect.width, 50)
            wizard_button_rect = pygame.Rect(self.panel_rect.x, self.panel_rect.y + 60, self.panel_rect.width, 50)

            if archer_button_rect.collidepoint(mouse_pos):
                self.handle_tower_type_selection("archer")
                return
            elif wizard_button_rect.collidepoint(mouse_pos):
                self.handle_tower_type_selection("wizard")
                return
        else:
            self.panel_visible = False

        rows, cols = len(self.map_data), len(self.map_data[0])
        start_x, start_y, block_unit = self.start_x, self.start_y, self.block_unit

        map_data = self.map_data

        for row in range(rows - 1):
            for col in range(cols - 2):
                if any(map_data[row + r][col + c] in [301, 302, 303, 304, 305, 306] for r in range(2) for c in range(3)):

                    if map_data[row][col] == 303:
                        tower_rect = pygame.Rect(start_x + col * block_unit, start_y + row * block_unit, 3* block_unit,
                                             2* block_unit)
                        if tower_rect.collidepoint(mouse_pos):
                            self.on_tower_click(row, col)

    def handle_square_click(self, row, col):
        print(f"Square clicked for tower at ({row}, {col})")

    def handle_tower_type_selection(self, tower_type):
        row, col = self.selected_tower_position
        base_texture_id = 311 if tower_type == "archer" else 321
        new_tower = Tower((row * self.block_unit, col * self.block_unit), tower_type)
        self.update_gold(-new_tower.cost)
        self.towers.append(new_tower)
        for i in range(3):  # Update three rows
            self.map_data[row][col + i] = base_texture_id + i
            self.map_data[row + 1][col + i] = base_texture_id + 3 + i

        self.panel_visible = False
        
    def on_tower_click(self, row, col):
        self.panel_visible = True
        self.selected_tower_position = (row, col)

    def draw_panel(self):
        if not self.panel_visible:
            return

        background_image = self.background_image

        self.screen.blit(background_image, (self.panel_rect.x, self.panel_rect.y))
        self.screen.blit(self.font.render("Archer", True, ui_color_black),
                         (self.panel_rect.x + 10, self.panel_rect.y + 10))
        self.screen.blit(background_image, (self.panel_rect.x, self.panel_rect.y + 60))
        self.screen.blit(self.font.render("Wizard", True, ui_color_black),
                         (self.panel_rect.x + 10, self.panel_rect.y + 70))

    def destroy_enemies_in_range(self):
        for tower in self.towers:
            enemies_to_remove, reward = tower.attack(self.enemies)
            for enemy in enemies_to_remove:
                self.enemies.remove(enemy)
                self.update_gold(reward)

    def draw(self):
        if self.freeze:
            self.screen.fill(ui_color_grass_100)
            self.draw_map()
            self.draw_end_menu()
            self.filter.draw()
            pygame.display.flip()
        else:
            # self.screen.fill(ui_color_grass)
            self.screen.fill(ui_color_grass_100)
            self.draw_map()
            # self.draw_towers()
            self.destroy_enemies_in_range()

            self.draw_enemies()


            for button, (x,y) in zip(self.navbar_buttons, self.navbar_positions):
                button.position = (x, y)
                button.draw()

            self.draw_panel()


            self.filter.draw()
            text = self.font.render("Score:" + str(fps), 1, (0, 0, 0))
            self.screen.blit(text, (150, 20))
            pygame.display.flip()

    def update(self):
        self.enemies_spawn_timer += 2
        if self.enemies_spawn_timer >= self.enemies_spawn_delay:
            if self.enemies_count < self.enemies_number:
                self.enemies_count += 1
                enemy = spawn_enemy(self, self.screen, self.animation_frames)
                self.enemies.append(enemy)
                self.enemies_spawn_timer = 0
        self.update_enemies()
        self.update_towers()
        self.draw_enemies()
        # self.draw_towers()

    def draw_end_menu(self):

        for button, (x, y) in zip(self.end_menu_buttons, self.end_menu_buttons_positions):
            button.position = (x, y)
            button.draw()

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