import pygame
import sys

def start_game(screen):
    pass

def open_settings(screen):
    pass

def quit_game():
    pygame.quit()
    sys.exit()

def draw_button(screen, text, position, size, action=None):
    font = pygame.font.Font(None, 40)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, (0, 0, 255), button_rect)
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (position[0] + (size[0] - label.get_width()) // 2, position[1] + (size[1] - label.get_height()) // 2))
    return button_rect

def scene_main_menu(screen):
    running = True
    while running:
        screen.fill((0, 0, 0))

        start_button = draw_button(screen, "Start Game", (300, 200), (200, 50))
        settings_button = draw_button(screen, "Settings", (300, 300), (200, 50))
        quit_button = draw_button(screen, "Close Game", (300, 400), (200, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return 'levels'
                elif settings_button.collidepoint(event.pos):
                    return 'settings'
                elif settings_button.collidepoint(event.pos):
                    open_settings(screen)
                elif quit_button.collidepoint(event.pos):
                    quit_game()


    pygame.quit()
