import json

import pygame
import sys

from ui.components.button import ui_button
from ui.filters.brightness import ui_brightness
from ui.layout.column import layout_column


class SceneLevels:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.levels = []

        # mC ~ mainConfig
        with open("data/config.json", "r") as mC:
            data = json.load(mC)
            self.levels = [level["title"] for level in data["levels"]]
            self.brightness_from_config = data["settings"]["brightness"]

        self.background_image = pygame.image.load("images/backgrounds/levels.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.filter = ui_brightness(self.screen, self.brightness_from_config)

        self.levels_buttons = [
            ui_button(self.screen, level, (0,0), (300,50), None, "button_vertical.png") for level in self.levels
        ]

        self.back_button = ui_button(screen, "back to main menu", (0, 0), (300, 50),  None, "button_vertical.png")

        self.buttons_to_layout = self.levels_buttons + [self.back_button]
        self.spacing = 20
        self.positions = layout_column(self.buttons_to_layout, self.width, self.height, self.spacing)

    def draw(self):
        self.screen.blit(self.background_image, (0,0))

        for button, (x, y) in zip(self.buttons_to_layout, self.positions):
            button.position = (x, y)
            button.draw()

        self.filter.draw()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return 'main_menu'
            for button, level in zip(self.levels_buttons, self.levels):
                if button.collidepoint(event.pos):
                    return f'game_{level}'

def scene_levels(screen):
    levels_scene = SceneLevels(screen)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene_action = levels_scene.handle_event(event)
                if scene_action:
                    return scene_action

        levels_scene.draw()

        pygame.display.flip()

    pygame.quit()