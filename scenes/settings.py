import pygame

from ui.components.button import ui_button

def scene_settings(screen):
    running = True
    while running:
        screen.fill((0, 0, 0))

        back_button = ui_button(screen, "back to main menu", (300, 200), (200, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return 'main_menu'

    pygame.quit()