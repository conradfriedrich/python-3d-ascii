import pygame
import numpy as np


def main():

    pygame.init()
    pygame.display.set_caption("minimal program")
    screen = pygame.display.set_mode((640, 480))
    screen.fill(pygame.Color(255, 255, 255))
    surf_array = pygame.surfarray.pixels3d(screen)
    print(np.size(surf_array, 0), np.size(surf_array, 1), np.size(surf_array, 2))
    surf_array[300:340, 220:260, :] = 0
    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


if __name__ == "__main__":
    main()
