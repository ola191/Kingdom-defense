import pygame

from scenes.main_menu import main_menu

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tower Defense")

def main():
    running = True
    while running:
        main_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
