from Game.Spirits.Enemy import Enemy

def spawn_enemy(self, screen, animation_frames):
    mapUnit = self.block_unit

    x, y = (self.startCord[1]) * mapUnit, self.startCord[0] * mapUnit
    return Enemy(screen,(x, y), "goblin", mapUnit, animation_frames)

