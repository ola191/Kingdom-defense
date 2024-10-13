import pygame

from ui.colors import *

class ui_brightness:
    def __init__(self, screen, brightness_level):
        self.screen = screen
        self.brightness_level = brightness_level
        self.brightness_filter = self.create_brightness_filter()

    def create_brightness_filter(self):
        brightness_filter = pygame.Surface(self.screen.get_size())
        brightness_filter.fill(ui_color_black)
        brightness_filter.set_alpha(255 - int(255 * (self.brightness_level / 100)))
        return brightness_filter


    def draw(self):
        if self.brightness_level < 25:
            self.brightness_level = 25

        self.screen.blit(self.brightness_filter, (0,0))

    def change_brightness(self, brightness_level):
        self.brightness_level = brightness_level