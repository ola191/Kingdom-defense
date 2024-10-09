import json
from sys import intern

import pygame

from ui.components.button import ui_button
from ui.components.slider import ui_slider
from ui.filters.brightness import ui_brightness
from ui.layout.column import layout_column


def scene_settings(screen):
    running = True

    width, height = screen.get_size()

    background_image = pygame.image.load("images/backgrounds/library.png")
    background_image = pygame.transform.scale(background_image, (width, height))

    with open("data/config.json", "r") as mC:
        data = json.load(mC)
        brightness_from_config = data["settings"]["brightness"]

    slider = ui_slider(screen, (750, 450), (400, 20), min_value=0, max_value=100, initial_value=brightness_from_config)

    back_button = ui_button(screen, "back to main menu", (300, 200), (300, 50), None, "button_vertical.png")

    buttons_to_layout = [back_button]

    spacing = 20
    available_width, available_height = screen.get_size()
    positions = layout_column(buttons_to_layout, available_width, available_height, spacing)

    filter = ui_brightness(screen, brightness_from_config)

    while running:
        screen.blit(background_image, (0,0))

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

        brightness_from_slider = slider.get_value()
        if brightness_from_slider != brightness_from_config:
            with open("data/config.json", "r") as mC:
                data = json.load(mC)
            data["settings"]["brightness"] = brightness_from_slider
            with open("data/config.json", "w") as mC:
                json.dump(data, mC, indent=4)
                ui_brightness.change_brightness(filter, brightness_from_slider)

        filter.draw()

        pygame.display.flip()

    pygame.quit()