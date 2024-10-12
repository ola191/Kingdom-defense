import pygame
import math

def spawn_enemy(self):
    mapUnit = self.block_unit
    self.update_gold("add")

    x, y = (self.startCord[1]) * mapUnit, self.startCord[0] * mapUnit
    enemy = {
        "rect": pygame.Rect(x, y, mapUnit, mapUnit),
        "path_index": 0
    }
    self.enemies.append(enemy)

def move_enemies(self):
    mapUnit = self.block_unit
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
