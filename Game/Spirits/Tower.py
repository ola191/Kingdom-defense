import math
import time


class Tower:
    def __init__(self, position, tower_type):
        self.position = position
        self.tower_type = tower_type
        self.range = None
        self.damage = None
        self.cooldown = None
        self.last_shot_time = 0

        self.create_param()

    def create_param(self):
        params = {
            "archer" : {
                "range" : 100,
                "damage": 50,
                "cooldown": 1.0
            },
            "wizard" : {
                "range" : 80,
                "damage": 120,
                "cooldown": 2.0
            }
        }

        type_params = params[f"{self.tower_type}"]

        self.range = type_params["range"]
        self.damage = type_params["damage"]
        self.cooldown = type_params["cooldown"]

    def attack(self,  enemies):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.cooldown:

            for enemy in enemies:
                if self.is_enemy_in_range(enemy):
                    enemy.take_damage(self.damage)
                    self.last_shot_time = current_time
                    break

    def is_enemy_in_range(self, enemy):
        distance = math.dist(self.position, enemmy.position)
        return distance <= self.range