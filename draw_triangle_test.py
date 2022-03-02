from dotmap import DotMap
import math


def main():
    points = [DotMap({"x": 5, "y": 1}), DotMap({"x": 1, "y": 10}), DotMap({"x": 7, "y": 4})]
    draw_filled_triangle(None, points, 0)


def draw_filled_triangle(canvas, points, color):
    # sort points by y coordinate
    points = sorted(points, key=lambda p: p.y)
    p0, p1, p2 = points
    x01 = interpolate(p0.y, p0.x, p1.y, p1.x)
    x12 = interpolate(p1.y, p1.x, p2.y, p2.x)
    x02 = interpolate(p0.y, p0.x, p2.y, p2.x)

    # Concatenate the short sides of the triangle
    x01.pop(-1)  # This would be counted twice
    x012 = x01 + x12

    # determine left and right
    m = math.floor(len(x012) / 2)
    if x02[m] < x012[m]:
        x_left = x02
        x_right = x012
    else:
        x_left = x012
        x_right = x02

    for y in range(p0.y, p2.y + 1):
        for x in range(x_left[y - p0.y], x_right[y - p0.y]):
            put_pixel(canvas, x, y, color)


def interpolate(i0, d0, i1, d1):
    if i0 == i1:
        return [d0]
    values = []

    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(i0, i1):
        values.append(int(d))
        d = d + a

    return values


if __name__ == "__main__":
    main()
