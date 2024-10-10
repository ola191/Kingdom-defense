import json

import pygame
import sys

from ui.animations import Animation
from ui.components.button import ui_button
from ui.filters.brightness import ui_brightness
from ui.layout.column import layout_column
from ui.navigators.button_navigator import Navigator


def start_game(screen):
    pass

def open_settings(screen):
    pass

def quit_game():
    pygame.quit()
    sys.exit()

class SceneMainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        self.background_image = pygame.image.load("images/backgrounds/mainmenu.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.selected_button = None
        with open("data/config.json", "r") as mC:
            data = json.load(mC)
            self.brightness_from_config = data["settings"]["brightness"]

        self.filter = ui_brightness(screen, self.brightness_from_config)

        self.start_button = ui_button(screen, "Start Game", (0, 0), (300, 50), self.sceneStart, "button_vertical.png", 80)
        self.settings_button = ui_button(screen, "Settings", (0, 0), (300, 50),  self.sceneSettings, "button_vertical.png", 100)
        self.quit_button = ui_button(screen, "Close Game", (0, 0), (300, 50),  quit_game, "button_vertical.png", 100)

        self.selected_button = self.start_button

        self.buttons_to_layout = [self.start_button, self.settings_button, self.quit_button]
        self.button_navigator = Navigator(self.buttons_to_layout)

        self.spacing = 20
        self.available_width, self.available_height = self.screen.get_size()
        self.positions = layout_column(self.buttons_to_layout, self.available_width, self.available_height, self.spacing)

        self.mixer = pygame.mixer
        self.mixer.init()

        self.click_sound = self.mixer.Sound("sounds/button_click.wav")

        self.button_navigator.update_selection()

    def sceneStart(self):
        return 'levels'
    def sceneSettings(self):
        return 'settings'

    def draw(self):
        self.screen.blit(self.background_image, (0,0))

        for button, (x,y) in zip(self.buttons_to_layout, self.positions):
            button.draw()

        self.filter.draw()

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                return self.start_button.action()
            elif self.settings_button.collidepoint(event.pos):
                return self.settings_button.action()
            elif self.quit_button.collidepoint(event.pos):
                self.quit_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.click_sound.play()
                self.button_navigator.next()
                self.selected_button = self.button_navigator.get_current()
            elif event.key == pygame.K_UP:
                self.click_sound.play()
                self.button_navigator.previous()
                self.selected_button = self.button_navigator.get_current()
            elif event.key == pygame.K_RETURN:
                self.click_sound.play()

                current_button = self.button_navigator.get_current()

                Animation.click_background(self.screen, 80, 40, 30, current_button, 200)

                if self.selected_button == self.start_button:
                    return 'levels'
                elif self.selected_button == self.settings_button:
                    return 'settings'
                elif self.selected_button == self.quit_button:
                    quit_game()

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()


def scene_main_menu(screen):
    main_menu_scene = SceneMainMenu(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene_action = main_menu_scene.handle_event(event)
                if scene_action:
                    return scene_action

        main_menu_scene.draw()
        pygame.display.flip()

    pygame.quit()