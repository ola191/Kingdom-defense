import pygame

from ui.colors import *

class ui_button:
    def __init__(self, screen, text, position, size, action=None, image=None):
        self.screen = screen
        self.text = text
        self.rect = pygame.Rect(position, size)
        self.position = position
        self.size = size
        self.image = image

    def draw(self):
        font = pygame.font.Font(None, 40)
        button_rect = pygame.Rect(self.position, self.size)
        if self.image is not None:
            if self.image == "button_vertical.png":
                background_image = pygame.image.load("images/ui/button_vertical.png")
                background_image = pygame.transform.scale(background_image, self.size)

                self.screen.blit(background_image, self.position)
            else:
                pygame.draw.rect(self.screen, ui_color_red, button_rect)
        else:
            pygame.draw.rect(self.screen, ui_color_white, button_rect)
        label = font.render(self.text, True, ui_color_black)
        self.screen.blit(label, (self.position[0] + (self.size[0] - label.get_width()) // 2, self.position[1] + (self.size[1] - label.get_height()) // 2))

    def get_size(self):
        return self.rect.size

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)