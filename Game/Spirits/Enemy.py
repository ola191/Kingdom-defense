import math
import time

import pygame

from ui.colors import ui_color_green, ui_color_red


class Enemy:
    def __init__(self, screen, position : tuple, enemy_type, block_unit, animation_frames):
        self.screen = screen
        self.animation_speed = 0.1
        self.position = position
        self.enemy_type = enemy_type
        self.max_health = None
        self.health = None
        self.speed = None
        self.reward = None
        self.alive = True
        self.path_index = 0
        self.create_param()

        self.animation_frames = animation_frames
        self.current_frame = 0
        self.block_unit = block_unit


    def update_animation(self):
        self.current_frame += self.animation_speed
        
        if self.current_frame >= len(self.animation_frames):
            self.current_frame = 0

    def draw(self, screen):
        if self.alive:
            x, y = self.position
            screen.blit(self.animation_frames[int(self.current_frame)], (x, y))

            full_live_rect = pygame.Rect((x + 25,y), (50, 10))
            pygame.draw.rect(self.screen, ui_color_red, full_live_rect)

            live_width = (self.health / self.max_health) * 50
            live_rect = pygame.Rect((x + 25 ,y), (live_width, 10))
            pygame.draw.rect(self.screen, ui_color_green, live_rect)
            self.update_animation()

    def create_param(self):
        params = {
            "goblin": {
                "health": 100,
                "speed": 1,
                "reward" : 25
            },
            "orc": {
                "health": 300,
                "speed": 0.75,
                "reward" : 75
            }
        }

        type_params = params[f"{self.enemy_type}"]

        self.max_health = type_params["health"]
        self.health = type_params["health"]
        self.speed = type_params["speed"]
        self.reward = type_params["reward"]

    def change_position(self, move_x, move_y):
        self.position[0] += move_x
        self.position[1] += move_y
        print(self.position[0], self.position[1])
    # def move(self):
    #     if self.alive:
    #         move_enemies(self)
    #         self.position = (self.position[0], self.position[1] + self.speed)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            reward = self.reward
            return False, reward
        else:
            return self.health, None

    def move_enemy(self, mSelf):
        mapUnit = mSelf.block_unit
        enemies_to_remove = []

        # for enemy in self.enemies:
        current_index = self.path_index
        if current_index < len(mSelf.path) - 1:
            next_point = mSelf.path[current_index + 1]

            target_x = next_point[1] * mapUnit
            target_y = next_point[0] * mapUnit
            dx = target_x - self.position[0]
            dy = target_y - self.position[1]

            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist > 0:
                move_x = self.speed * (dx /dist)
                move_y = self.speed * (dy /dist)

                self.position = (self.position[0] + move_x, self.position[1] + move_y)

                if dist <= self.speed:
                    self.position = (target_x, target_y)
                    self.path_index += 1
            else:
                self.path_index += 1
            # print(dist)
            # if dist != 0:
            #     move_x = self.speed * (dx / dist)
            #     move_y = self.speed * (dy / dist)
            # else:
            #     move_x, move_y = 0, 0
            #     self.path_index += 1
            #
            # self.position = (self.position[0] + move_x, self.position[1] + move_y)
            # #
            # # if abs(self.position[0] - target_x) < self.speed and abs(
            # #         self.position[1] - target_y) < self.speed:
            # #     self.speed += 1
        else:
            mSelf.enemies.remove(self)
            return -1
