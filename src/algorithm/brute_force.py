def brute_force(x1: int, x2: int, y1: int, y2: int) -> list[tuple[int, int]]:
    pixels_to_draw: list[tuple[int, int]] = []  
    del_y = y2 - y1
    del_x = x2 - x1

    if del_x == 0 and del_y == 0:
        return [(x1, y1)]

    if abs(del_x) >= abs(del_y):
        m = del_y / del_x
        c = y1 - (m * x1)
        step = 1 if x2 >= x1 else -1

        for x in range(x1, x2 + step, step):
            y = round(m * x + c)
            pixels_to_draw.append((x, y))
    else:
        m = del_x / del_y
        c = x1 - (m * y1)
        step = 1 if y2 >= y1 else -1

        for y in range(y1, y2 + step, step):
            x = round(m * y + c)
            pixels_to_draw.append((x, y))

    return pixels_to_draw
        

        
