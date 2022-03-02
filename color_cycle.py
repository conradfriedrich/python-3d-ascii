import pygame
import math


def main():

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("minimal program")
    # create a surface on screen that has the size of 240 x 180

    screen = pygame.display.set_mode((1980, 1080))
    derp = 5
    # r,g,b = randint(0,255), randint(0,255), randint(0,255)

    running = True
    cos_phase = 0
    step = 0.001
    r, g, b = 0, 0, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        r = cos_to_rgb(math.cos(cos_phase))
        g = cos_to_rgb(math.cos(cos_phase + math.pi / 2))
        b = cos_to_rgb(math.cos(cos_phase + math.pi))
        print("%s %s %s" % (r, g, b))
        screen.fill(pygame.Color(round(r), round(g), round(b)))
        pygame.display.flip()

        cos_phase += step
        if cos_phase > 2 * math.pi:
            cos_phase = 0


def cos_to_rgb(cos):
    return 124.5 * (cos + 1)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
