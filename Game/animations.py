import pygame

def load_animation(animation_name, block_unit):
    if animation_name == "goblin":
        animation_frames = []
        for i in range(3):
            tileset_image = pygame.image.load(f"images/monsters/sprite_{i}.png").convert_alpha()
            tileset_image = pygame.transform.scale(tileset_image, (block_unit * 9, block_unit * 9))

            rect = pygame.Rect(block_unit * 6, block_unit * 6, block_unit * 3, block_unit * 3)

            animation_frames.append(tileset_image.subsurface(rect))

        return animation_frames