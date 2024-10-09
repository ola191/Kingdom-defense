import pygame

from ui.components.button import ui_button
from ui.layout.column import layout_column


def scene_settings(screen):
    running = True
    while running:
        screen.fill((0, 0, 0))

        back_button = ui_button(screen, "back to main menu", (300, 200), (300, 50),  None, "button_vertical.png")

        buttons_to_layout = [back_button]

        spacing = 20
        available_width, available_height = screen.get_size()
        positions = layout_column(buttons_to_layout, available_width, available_height, spacing)

        for button, (x, y) in zip(buttons_to_layout, positions):
            button.position = (x, y)
            button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return 'main_menu'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_menu'

    pygame.quit()