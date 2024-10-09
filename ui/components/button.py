import pygame

from ui.colors import *

class ui_button:
    def __init__(self, screen, text, position, size, action=None):
        self.screen = screen
        self.text = text
        self.rect = pygame.Rect(position, size)
        self.position = position
        self.size = size

    def draw(self):
        font = pygame.font.Font(None, 40)
        button_rect = pygame.Rect(self.position, self.size)
        pygame.draw.rect(self.screen, ui_color_white, button_rect)
        label = font.render(self.text, True, ui_color_black)
        self.screen.blit(label, (self.position[0] + (self.size[0] - label.get_width()) // 2, self.position[1] + (self.size[1] - label.get_height()) // 2))

    def get_size(self):
        return self.rect.size

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)