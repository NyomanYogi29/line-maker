def line(x1: int, x2: int, y1: int, y2: int) -> list[tuple[int, int]]:
    pixels_to_draw: list[tuple[int, int]] = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    x, y = x1, y1

    if dx >= dy:
        p = 2 * dy - dx

        for _ in range(dx + 1):
            pixels_to_draw.append((x, y))

            if p >= 0:
                y += sy
                p += 2 * (dy - dx)
            else:
                p += 2 * dy

            x += sx
    else:
        p = 2 * dx - dy

        for _ in range(dy + 1):
            pixels_to_draw.append((x, y))

            if p >= 0:
                x += sx
                p += 2 * (dx - dy)
            else:
                p += 2 * dx
            y += sy

    return pixels_to_draw

def circle(xc: int, yc: int, r: int) -> list[tuple[int, int]]:
    pixels_to_draw: list[tuple[int, int]] = []

    x = 0
    y = r

    p = 1 - r

    def plot_symmetric_points(cx: int, cy: int, px: int, py: int) -> None:
        # Reflect onto 8th octant
        pixels_to_draw.extend([                                                                                                                      
            (cx + px, cy + py),                                                                                                                      
            (cx - px, cy + py),                                                                                                                      
            (cx + px, cy - py),                                                                                                                      
            (cx - px, cy - py),                                                                                                                      
            (cx + py, cy + px),                                                                                                                      
            (cx - py, cy + px),                                                                                                                      
            (cx + py, cy - px),                                                                                                                      
            (cx - py, cy - px),                                                                                                                      
        ])

    plot_symmetric_points(xc, yc, x, y)

    while x < y:
        x += 1

        # Midpoint inside the circle -> y remain constant
        if p < 0:
            p += 2 * x + 1

        # Midpoint outside the circle -> y moves down by 1 step
        else:
            y -= 1
            p += 2 * x + 1 - 2 * y

        plot_symmetric_points(xc, yc, x, y)

    return pixels_to_draw