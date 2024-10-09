import pygame

from ui.components.button import ui_button
from ui.components.slider import ui_slider
from ui.layout.column import layout_column


def scene_settings(screen):
    running = True

    width, height = screen.get_size()

    background_image = pygame.image.load("images/backgrounds/library.png")
    background_image = pygame.transform.scale(background_image, (width, height))

    slider = ui_slider(screen, (200, 300), (400, 20), min_value=0, max_value=100, initial_value=50)

    while running:
        screen.blit(background_image, (0,0))

        back_button = ui_button(screen, "back to main menu", (300, 200), (300, 50),  None, "button_vertical.png")

        buttons_to_layout = [back_button]

        spacing = 20
        available_width, available_height = screen.get_size()
        positions = layout_column(buttons_to_layout, available_width, available_height, spacing)

        for button, (x, y) in zip(buttons_to_layout, positions):
            button.position = (x, y)
            button.draw()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return 'main_menu'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_menu'

            slider.handle_event(event)
        slider.draw()
        brightness = slider.get_value()
        print(f"brightness: {brightness}%")

        pygame.display.flip()

    pygame.quit()