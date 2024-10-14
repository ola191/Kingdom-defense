import pygame

def load_texture(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)

textures = {
    "grass_01": lambda size: load_texture("images/textures/grass_1.jpg", size),
    "grass_02": lambda size: load_texture("images/textures/grass_2.jpg", size),
    "grass_03": lambda size: load_texture("images/textures/grass_3.jpg", size),
    "path_01": lambda size: load_texture("images/textures/path_1.jpg", size),
    "tower_01": lambda size: load_texture("images/textures/tower_1.jpg", size),
    "tower_02": lambda size: load_texture("images/textures/tower_2.jpg", size),
    "tower_03": lambda size: load_texture("images/textures/tower_3.jpg", size),
    "tower_04": lambda size: load_texture("images/textures/tower_4.jpg", size),
    "tower_05": lambda size: load_texture("images/textures/tower_5.jpg", size),
    "tower_06": lambda size: load_texture("images/textures/tower_6.jpg", size),
    "tower_archer_01" : lambda size: load_texture("images/textures/tower_1_empty.jpg", size),
    "tower_archer_02": lambda size: load_texture("images/textures/tower_2_empty.jpg", size),
    "tower_archer_03": lambda size: load_texture("images/textures/tower_3_empty.jpg", size),
    "tower_archer_04": lambda size: load_texture("images/textures/tower_4_empty.jpg", size),
    "tower_archer_05": lambda size: load_texture("images/textures/tower_5_empty.jpg", size),
    "tower_archer_06": lambda size: load_texture("images/textures/tower_6_empty.jpg", size),
}

def get_texture(name, size):
    return textures[name](size)