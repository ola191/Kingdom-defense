import pygame
import math

from Game.Spirits.Enemy import Enemy


def spawn_enemy(self):
    mapUnit = self.block_unit
    self.update_gold("add")

    x, y = (self.startCord[1]) * mapUnit, self.startCord[0] * mapUnit
    # enemy = {
        # "rect": pygame.Rect(x, y, mapUnit, mapUnit),
        # "path_index": 0
    # }
    return Enemy((x, y), "goblin")

def move_enemy(self, enemy):
    mapUnit = self.block_unit
    enemies_to_remove = []


    # for enemy in self.enemies:
    current_index = enemy.path_index

    if current_index < len(self.path) - 1:
        next_point = self.path[current_index + 1]

        target_x = next_point[1] * mapUnit
        target_y = next_point[0] * mapUnit

        dx = target_x - enemy.position[0]
        dy = target_y - enemy.position[1]

        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist != 0:
            move_x = enemy.speed * (dx / dist)
            move_y = enemy.speed * (dy / dist)
        else:
            move_x, move_y = 0, 0

        enemy.change_position = (move_x, move_y)

        if abs(enemy.position[0] - target_x) < enemy.speed and abs(
                enemy.position[1] - target_y) < enemy.speed:
            enemy.speed += 1
    else:
        enemies_to_remove.append(enemy)
    # for enemy in enemies_to_remove:
    self.enemies.remove(enemy)
