import json
from sys import intern

import pygame

from ui.components.button import ui_button
from ui.components.slider import ui_slider
from ui.filters.brightness import ui_brightness
from ui.layout.column import layout_column


class SceneLibrary:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()


        self.background_image = pygame.image.load("images/backgrounds/library.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        with open("data/config.json", "r") as mC:
            data = json.load(mC)
            self.brightness_from_config = data["settings"]["brightness"]

        self.filter = ui_brightness(screen, self.brightness_from_config)

    def draw(self):
        self.screen.blit(self.background_image, (0,0))

        self.filter.draw()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'levels'

    def update(self):
        pass

def scene_library(screen):
    settings_scene = SceneLibrary(screen)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene_action = settings_scene.handle_events(event)
                if scene_action:
                    return scene_action

        settings_scene.draw()
        settings_scene.update()

        pygame.display.flip()

    pygame.quit()