import json

import pygame

from ui.components.button import ui_button
from ui.components.slider import ui_slider
from ui.filters.brightness import ui_brightness
from ui.layout.column import layout_column
from ui.navigators.button_navigator import Navigator

class SceneSettings:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.background_image = pygame.image.load("images/backgrounds/prison.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        with open("data/config.json", "r") as mC:
            data = json.load(mC)
            self.brightness_from_config = data["settings"]["brightness"]

        self.slider = ui_slider(screen, (750, 450), (400, 20), min_value=0, max_value=100, initial_value=self.brightness_from_config)
        self.back_button = ui_button(screen, "back to main menu", (300, 200), (300, 50), None, "button_vertical.png")

        self.elements_to_layout = [self.slider, self.back_button]
        self.navigator = Navigator(self.elements_to_layout)

        self.spacing = 20
        self.available_width, self.available_height = self.screen.get_size()
        self.positions = layout_column(self.elements_to_layout, self.available_width, self.available_height, self.spacing)

        self.filter = ui_brightness(screen, self.brightness_from_config)

    def draw(self):
        self.screen.blit(self.background_image, (0,0))

        for element, (x, y) in zip(self.elements_to_layout, self.positions):
            element.position = (x, y)
            element.draw()

        self.filter.draw()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return 'main_menu'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'main_menu'
        scene_action = self.navigator.handle_event(event)
        if scene_action:
            return scene_action

    def update(self):
        self.brightness_from_slider = self.slider.get_value()
        if self.brightness_from_slider != self.brightness_from_config:
            with open("data/config.json", "r") as mC:
                data = json.load(mC)
            data["settings"]["brightness"] = self.brightness_from_slider
            with open("data/config.json", "w") as mC:
                json.dump(data, mC, indent=4)
                ui_brightness.change_brightness(self.filter, self.brightness_from_slider)

def scene_settings(screen):
    settings_scene = SceneSettings(screen)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene_action = settings_scene.handle_events(event)
                if scene_action == "main_menu":
                    return "main_menu"

        settings_scene.draw()
        settings_scene.update()

        pygame.display.flip()

    pygame.quit()