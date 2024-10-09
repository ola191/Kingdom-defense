import pygame

from scenes.main_menu import scene_main_menu
from scenes.levels import scene_levels
from scenes.settings import scene_settings

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tower Defense")

def main():
    running = True
    game_scene = "main_menu"
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_scene == "main_menu":
            selected_scene = scene_main_menu(screen)
            if selected_scene:
                game_scene = selected_scene
        elif game_scene == "levels":
            selected_scene = scene_levels(screen)
            if selected_scene:
                game_scene = selected_scene
        elif game_scene == "settings":
            selected_scene = scene_settings(screen)
            if selected_scene:
                game_scene = selected_scene

    pygame.quit()

if __name__ == "__main__":
    main()
