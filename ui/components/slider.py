import pygame

from ui.colors import ui_color_white, ui_color_black, ui_color_red
from ui.components.button import ui_button


class ui_slider:
    def __init__(self, screen, position, size, min_value=0, max_value=100, initial_value=50):
        self.screen = screen
        self.rect = pygame.Rect(position, size)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value

        self.handle_rect = pygame.Rect(0, 0, 20, size[1] + 10)
        self.handle_rect.centerx = self.rect.left + (self.value / self.max_value) * self.rect.width
        self.handle_rect.centery = self.rect.centery
        self.dragging = False

    def draw(self):
        pygame.draw.rect(self.screen, ui_color_white, self.rect)
        pygame.draw.rect(self.screen, ui_color_black, self.rect, 2)

        self.handle_rect.centerx = self.rect.left + (self.value / self.max_value) * self.rect.width
        pygame.draw.rect(self.screen, ui_color_black, self.handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_rect.centerx = min(max(event.pos[0], self.rect.left), self.rect.right)
            self.value = int(((self.handle_rect.centerx - self.rect.left) / self.rect.width) * self.max_value)

    def get_value(self):
        if self.value < 25:
            return 25
        return self.value
