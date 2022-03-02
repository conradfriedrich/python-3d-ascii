# TODO implement the conversion between centered and display coordinates
# TODO add full range color before moving on

import pygame
import numpy as np
import math


def main():
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 270
    SCALE_UP_FACTOR = 4

    pygame.init()
    pygame.display.set_caption("minimal program")
    screen = pygame.display.set_mode((SCREEN_WIDTH * SCALE_UP_FACTOR, SCREEN_HEIGHT * SCALE_UP_FACTOR))

    surface = pygame.Surface(screen.get_size())
    surface.fill(pygame.Color(255, 255, 255))
    surf_array = pygame.surfarray.pixels3d(surface)

    engine = Engine_3d(surf_array, screen)

    p = [0, 0]
    cos_phase = 0
    step = 0.1
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # Draw blank white
        engine.wipe([255, 255, 255])

        p0 = (
            round(100 * math.cos(cos_phase + math.pi / 2) - 200),
            round(50 * math.sin(cos_phase - math.pi / 2) + 100),
        )
        p1 = (round(70 * math.cos(cos_phase + math.pi) - 0), round(50 * math.sin(cos_phase - math.pi) - 30))
        p2 = (round(20 * math.cos(cos_phase) + 200), round(100 * math.sin(cos_phase) + 160))

        points = [p0, p1, p2]

        engine.draw_shaded_triangle(points, [139, 211, 239])
        engine.draw_wireframe_triangle(points, [100, 100, 100])

        engine.update()

        cos_phase += step
        if cos_phase > 2 * math.pi:
            cos_phase = 0


class Engine_3d:
    def __init__(self, canvas, screen):
        self.canvas = canvas
        self.screen = screen

    def draw_line(self, p0, p1, color):
        x0 = p0[0]
        y0 = p0[1]
        x1 = p1[0]
        y1 = p1[1]
        # check for horizontal-like vs. vertical-like line
        if abs(x1 - x0) > abs(y1 - y0):
            # ensure that x0 < x1, otherwise swap p0 and p1
            if x0 > x1:
                return self.draw_line(p1, p0, color)
            ys = self.interpolate(x0, y0, x1, y1)
            for x in range(x0, x1):
                self.put_pixel(x, ys[x - x0], color)
        else:
            if y0 > y1:
                return self.draw_line(p1, p0, color)
            xs = self.interpolate(y0, x0, y1, x1)
            for y in range(y0, y1):
                self.put_pixel(xs[y - y0], y, color)

    def draw_wireframe_triangle(self, points, color):
        self.draw_line(points[0], points[1], color)
        self.draw_line(points[1], points[2], color)
        self.draw_line(points[2], points[0], color)

    def draw_filled_triangle(self, points, color):
        # sort points by y coordinate
        points = sorted(points, key=lambda p: p[1])
        p0, p1, p2 = points
        x01 = self.interpolate(points[0][1], points[0][0], points[1][1], points[1][0])
        x12 = self.interpolate(points[1][1], points[1][0], points[2][1], points[2][0])
        x02 = self.interpolate(points[0][1], points[0][0], points[2][1], points[2][0])

        # Concatenate the short sides of the triangle
        x012 = x01 + x12

        # determine left and right
        m = math.floor(len(x012) / 2)
        if x02[m] < x012[m]:
            x_left = x02
            x_right = x012
        else:
            x_left = x012
            x_right = x02

        for y in range(points[0][1], points[2][1]):
            for x in range(x_left[y - points[0][1]], x_right[y - points[0][1]]):
                self.put_pixel(x, y, color)

    def draw_shaded_triangle(self, points, color):
        # sort points by y coordinate
        points = sorted(points, key=lambda p: p[1])
        p0, p1, p2 = points
        h0, h1, h2 = [0.0, 0.5, 1.0]
        x01 = self.interpolate(points[0][1], points[0][0], points[1][1], points[1][0])
        h01 = self.interpolate(points[0][1], h0, points[1][1], h1)

        x12 = self.interpolate(points[1][1], points[1][0], points[2][1], points[2][0])
        h12 = self.interpolate(points[1][1], h1, points[2][1], h2)

        x02 = self.interpolate(points[0][1], points[0][0], points[2][1], points[2][0])
        h02 = self.interpolate(points[0][1], h0, points[2][1], h2)
        # Concatenate the short sides of the triangle
        x012 = x01 + x12
        h012 = h01 + h12

        # determine left and right
        m = math.floor(len(x012) / 2)
        if x02[m] < x012[m]:
            x_left = x02
            h_left = h02

            x_right = x012
            h_right = h012
        else:
            x_left = x012
            h_left = h012

            x_right = x02
            h_right = h02

        for y in range(points[0][1], points[2][1]):
            x_l = int(x_left[y - points[0][1]])
            x_r = int(x_right[y - points[0][1]])
            h_segment = self.interpolate(x_l, h_left[y - points[0][1]], x_r, h_right[y - points[0][1]])
            for x in range(x_l, x_r):
                shaded_color = self.shade_color(color, h_segment[x - x_l])
                self.put_pixel(x, y, shaded_color)

    def shade_color(self, color, shade):
        color = [c * shade for c in color]
        return color

    def interpolate(self, i0, d0, i1, d1):
        i0 = int(i0)
        i1 = int(i1)
        if i0 == i1:
            return [d0]
        values = []

        a = (d1 - d0) / (i1 - i0)
        d = d0
        for i in range(i0, i1):
            # values.append(int(d))
            values.append(d)
            d = d + a

        return values

    def put_pixel(self, x, y, color):
        # Convert centered coordinates to origin top left
        canvas_width = np.shape(self.canvas)[0]
        canvas_height = np.shape(self.canvas)[1]
        x = canvas_width / 2 + x
        y = canvas_height / 2 - y
        self.canvas[int(x), int(y), 0] = color[0]
        self.canvas[int(x), int(y), 1] = color[1]
        self.canvas[int(x), int(y), 2] = color[2]

    def wipe(self, color):
        self.canvas[:, :, 0] = color[0]
        self.canvas[:, :, 1] = color[1]
        self.canvas[:, :, 2] = color[2]

    def update(self):
        pygame.surfarray.blit_array(self.screen, self.canvas)
        pygame.display.update()


if __name__ == "__main__":
    main()
