def DDA(x1: int, x2: int, y1: int, y2: int) -> list[tuple[int, int]]:
    pixels_to_draw: list[tuple[int, int]] = []
    
    del_x = x2 - x1
    del_y = y2 - y1

    steps = max(abs(del_x), abs(del_y))

    if steps == 0:
        return [(x1, y1)]

    x_inc = del_x/steps
    y_inc = del_y/steps

    x = float(x1)
    y = float(y1)

    for _ in range(steps + 1):
        pixels_to_draw.append((round(x), round(y)))
        x += x_inc
        y += y_inc

    return pixels_to_draw
    

    

