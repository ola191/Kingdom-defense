import pygame
import sys

from ui.button import ui_button

def start_game(screen):
    pass

def open_settings(screen):
    pass

def quit_game():
    pygame.quit()
    sys.exit()

def scene_main_menu(screen):
    running = True
    while running:
        screen.fill((0, 0, 0))

        start_button = ui_button(screen, "Start Game", (300, 200), (200, 50))
        settings_button = ui_button(screen, "Settings", (300, 300), (200, 50))
        quit_button = ui_button(screen, "Close Game", (300, 400), (200, 50))

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
