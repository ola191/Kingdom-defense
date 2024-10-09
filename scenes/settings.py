import pygame
import sys

def draw_button(screen, text, position, size, action=None):
    font = pygame.font.Font(None, 40)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, (0, 0, 255), button_rect)
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (position[0] + (size[0] - label.get_width()) // 2, position[1] + (size[1] - label.get_height()) // 2))
    return button_rect

def scene_settings(screen):
    running = True
    while running:
        screen.fill((0, 0, 0))

        back_button = draw_button(screen, "back to main menu", (300, 200), (200, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return 'main_menu'

    pygame.quit()