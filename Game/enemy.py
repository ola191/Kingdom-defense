import pygame
import math

from Game.Spirits.Enemy import Enemy


def spawn_enemy(self, animation_frames):
    mapUnit = self.block_unit

    x, y = (self.startCord[1]) * mapUnit, self.startCord[0] * mapUnit
    # enemy = {
        # "rect": pygame.Rect(x, y, mapUnit, mapUnit),
        # "path_index": 0
    # }
    return Enemy((x, y), "goblin", mapUnit, animation_frames)

