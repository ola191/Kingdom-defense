import pygame

from ui.colors import *

def ui_button(screen, text, position, size, action=None):
    font = pygame.font.Font(None, 40)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, ui_color_white, button_rect)
    label = font.render(text, True, ui_color_black)
    screen.blit(label, (position[0] + (size[0] - label.get_width()) // 2, position[1] + (size[1] - label.get_height()) // 2))
    return button_rect