import pygame

from ui.colors import *

class ui_button:
    def __init__(self, screen, text, position, size, action=None, image=None, brightness=100):
        self.screen = screen
        self.text = text
        self.rect = pygame.Rect(position, size)
        self.position = position
        self.size = size
        self.image = image
        self.brightness = brightness
        self.selected = False
        self.action = action

        self.images = {
            "button_vertical.png" : pygame.transform.scale((pygame.image.load("images/ui/button_vertical.png").convert_alpha()), self.size)
        }

        self.brightness_filter = self.create_brightness_filter()

    def create_brightness_filter(self):
        self.brightness_filter = pygame.Surface(self.get_size())
        self.brightness_filter.fill(ui_color_black)
        self.brightness_filter.set_alpha(255 - int(255 * (self.brightness / 100)))
        return self.brightness_filter

    def draw(self):
        font = pygame.font.Font(None, 40)
        button_rect = pygame.Rect(self.position, self.size)
        if self.image is not None:
            self.screen.blit(self.images[self.image], self.position)
        else:
            pygame.draw.rect(self.screen, ui_color_white, button_rect)
        label = font.render(self.text, True, ui_color_black)
        self.screen.blit(label, (self.position[0] + (self.size[0] - label.get_width()) // 2, self.position[1] + (self.size[1] - label.get_height()) // 2))


        self.screen.blit(self.brightness_filter, self.position)


    def get_size(self):
        return self.rect.size

    def change_brightness(self, brightness):
        self.brightness = brightness

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)