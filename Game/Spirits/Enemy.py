import math
import time

class Enemy:
    def __init__(self, position : tuple, enemy_type):
        self.position = position
        self.enemy_type = enemy_type
        self.health = None
        self.speed = None
        self.alive = True
        self.path_index = 0
        self.create_param()

    def create_param(self):
        params = {
            "goblin": {
                "health": 100,
                "speed": 1,
            },
            "orc": {
                "health": 300,
                "speed": 0.75
            }
        }

        type_params = params[f"{self.enemy_type}"]

        self.health = type_params["health"]
        self.speed = type_params["speed"]

    def change_position(self, move_x, move_y):
        self.position[0] += move_x
        self.position[1] += move_y

    # def move(self):
    #     if self.alive:
    #         move_enemies(self)
    #         self.position = (self.position[0], self.position[1] + self.speed)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False