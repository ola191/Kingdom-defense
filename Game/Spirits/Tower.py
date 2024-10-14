import math
import time

class Tower:
    def __init__(self, position, tower_type):
        self.position = position
        self.tower_type = tower_type
        self.range = None
        self.damage = None
        self.cooldown = None
        self.cost = None
        self.last_shot_time = 0
        self.create_param()

    def create_param(self):
        params = {
            "archer" : {
                "range" : 400,
                "damage": 25,
                "cooldown": 1,
                "cost" : 100
            },
            "wizard" : {
                "range" : 350,
                "damage": 120,
                "cooldown": 2,
                "cost" : 150
            }
        }

        type_params = params[f"{self.tower_type}"]

        self.range = type_params["range"]
        self.damage = type_params["damage"]
        self.cooldown = type_params["cooldown"]
        self.cost = type_params["cost"]

    def attack(self,  enemies):
        current_time = time.time()

        enemies_to_remove = []
        reward = 0
        if current_time - self.last_shot_time >= self.cooldown:
            for enemy in enemies:
                if self.is_enemy_in_range(enemy):
                    isAlive, reward = enemy.take_damage(self.damage)
                    if not isAlive:
                        reward += reward
                        enemies_to_remove.append(enemy)

                    self.last_shot_time = current_time
                    break
        return enemies_to_remove, reward

    def is_enemy_in_range(self, enemy):
        distance = math.dist(self.position, enemy.position)
        return distance <= self.range