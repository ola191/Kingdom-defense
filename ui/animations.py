import pygame

class Animation:
    @staticmethod
    def click_background(screen, range_from, range_to, steps, element, duration):
        scope = range_from - range_to
        change_per_step = scope / steps

        start_time = pygame.time.get_ticks()
        elapsed_time = 0

        while elapsed_time < duration:
            elapsed_time = pygame.time.get_ticks() - start_time
            current_step = min(steps, int(elapsed_time / (duration / steps)))

            element.brightness = range_from - current_step * change_per_step

            element.draw()
            pygame.display.flip()

            pygame.time.delay(16)