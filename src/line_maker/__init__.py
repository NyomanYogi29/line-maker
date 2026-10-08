import math
import pygame
from algorithm import brute_force
from algorithm import dda
from algorithm import bresenham

ALGORITHMS = {
    1: "Brute Force - Garis",
    2: "DDA - Garis",
    3: "Bresenham - Garis",
    4: "Bresenham - Lingkaran",
}

ALGORITHM_MODES = {
    pygame.K_1: ALGORITHMS[1],
    pygame.K_2: ALGORITHMS[2],
    pygame.K_3: ALGORITHMS[3],
    pygame.K_4: ALGORITHMS[4],
}


def main() -> None:
    pygame.init()
    screen_width, screen_height = 1280, 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Line Maker - Virtual Pixel Grid")
    font = pygame.font.Font(None, 24)
    info_font = pygame.font.Font(None, 20)
    clock = pygame.time.Clock()

    grid_cols, grid_rows = 400, 400
    # Store discrete logical pixels where 1 pixel equals 1 grid cell
    grid_surface = pygame.Surface((grid_cols, grid_rows))
    grid_surface.fill((255, 255, 255))

    cell_size = 8.0
    offset_x = (screen_width - grid_cols * cell_size) / 2
    offset_y = (screen_height - grid_rows * cell_size) / 2

    is_panning = False
    pan_start_pos = (0, 0)
    pan_start_offset = (offset_x, offset_y)

    current_mode = ALGORITHMS[1]
    toast_message = f"Mode: {current_mode}"
    toast_start_time = pygame.time.get_ticks()

    start_grid_point: tuple[int, int] | None = None
    running = True

    def screen_to_grid(sx: int, sy: int) -> tuple[int, int]:
        gx = int((sx - offset_x) // cell_size)
        gy = int((sy - offset_y) // cell_size)
        return gx, gy

    while running:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in ALGORITHM_MODES:
                    current_mode = ALGORITHM_MODES[event.key]
                    toast_message = f"Mode: {current_mode}"
                    toast_start_time = current_time
                    start_grid_point = None

            elif event.type == pygame.MOUSEWHEEL:
                old_cell_size = cell_size
                if event.y > 0:
                    cell_size = min(cell_size * 1.15, 60.0)
                elif event.y < 0:
                    cell_size = max(cell_size / 1.15, 1.0)

                # Keep cursor point stable during zoom
                mx, my = mouse_pos
                offset_x = mx - (mx - offset_x) * (cell_size / old_cell_size)
                offset_y = my - (my - offset_y) * (cell_size / old_cell_size)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gx, gy = screen_to_grid(event.pos[0], event.pos[1])
                    if 0 <= gx < grid_cols and 0 <= gy < grid_rows:
                        if start_grid_point is None:
                            start_grid_point = (gx, gy)
                            print(f"[{current_mode}] Start Grid Point: {start_grid_point}")
                        else:
                            end_grid_point = (gx, gy)
                            print(f"[{current_mode}] End Grid Point  : {end_grid_point}")
                            pixels: list[tuple[int, int]] = []

                            if current_mode == ALGORITHMS[1]:
                                pixels = brute_force.brute_force(
                                    start_grid_point[0], end_grid_point[0],
                                    start_grid_point[1], end_grid_point[1]
                                )
                            elif current_mode == ALGORITHMS[2]:
                                pixels = dda.DDA(
                                    start_grid_point[0], end_grid_point[0],
                                    start_grid_point[1], end_grid_point[1]
                                )
                            elif current_mode == ALGORITHMS[3]:
                                pixels = bresenham.line(
                                    start_grid_point[0], end_grid_point[0],
                                    start_grid_point[1], end_grid_point[1]
                                )
                            elif current_mode == ALGORITHMS[4]:
                                dx = end_grid_point[0] - start_grid_point[0]
                                dy = end_grid_point[1] - start_grid_point[1]
                                radius = round(math.hypot(dx, dy))
                                pixels = bresenham.circle(start_grid_point[0], start_grid_point[1], radius)

                            if pixels:
                                print(f"Total piksel terlukis: {len(pixels)}")

                            for px, py in pixels:
                                if 0 <= px < grid_cols and 0 <= py < grid_rows:
                                    grid_surface.set_at((px, py), (20, 20, 20))

                            start_grid_point = None

                elif event.button == 3:
                    is_panning = True
                    pan_start_pos = event.pos
                    pan_start_offset = (offset_x, offset_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    is_panning = False

            elif event.type == pygame.MOUSEMOTION:
                if is_panning:
                    dx = event.pos[0] - pan_start_pos[0]
                    dy = event.pos[1] - pan_start_pos[1]
                    offset_x = pan_start_offset[0] + dx
                    offset_y = pan_start_offset[1] + dy

        screen.fill((235, 238, 242))

        # Viewport culling: only scale visible cells to keep memory and CPU usage near zero
        vis_col_start = max(0, int(-offset_x // cell_size))
        vis_col_end = min(grid_cols, int((screen_width - offset_x) // cell_size) + 1)
        vis_row_start = max(0, int(-offset_y // cell_size))
        vis_row_end = min(grid_rows, int((screen_height - offset_y) // cell_size) + 1)

        if vis_col_end > vis_col_start and vis_row_end > vis_row_start:
            sub_rect = pygame.Rect(
                vis_col_start,
                vis_row_start,
                vis_col_end - vis_col_start,
                vis_row_end - vis_row_start,
            )
            sub_surface = grid_surface.subsurface(sub_rect)

            target_w = int(sub_rect.width * cell_size)
            target_h = int(sub_rect.height * cell_size)
            scaled_sub = pygame.transform.scale(sub_surface, (target_w, target_h))

            draw_x = int(offset_x + vis_col_start * cell_size)
            draw_y = int(offset_y + vis_row_start * cell_size)
            screen.blit(scaled_sub, (draw_x, draw_y))

        scaled_w = int(grid_cols * cell_size)
        scaled_h = int(grid_rows * cell_size)
        canvas_rect = pygame.Rect(int(offset_x), int(offset_y), scaled_w, scaled_h)
        pygame.draw.rect(screen, (100, 100, 100), canvas_rect, 1)

        # Draw grid lines only when cells are large enough to avoid visual clutter
        if cell_size >= 6.0:
            grid_color = (220, 220, 220)
            start_col = max(0, int(-offset_x // cell_size))
            end_col = min(grid_cols, int((screen_width - offset_x) // cell_size) + 1)
            start_row = max(0, int(-offset_y // cell_size))
            end_row = min(grid_rows, int((screen_height - offset_y) // cell_size) + 1)

            for col in range(start_col, end_col + 1):
                x = int(offset_x + col * cell_size)
                y1 = max(0, int(offset_y))
                y2 = min(screen_height, int(offset_y + scaled_h))
                pygame.draw.line(screen, grid_color, (x, y1), (x, y2))

            for row in range(start_row, end_row + 1):
                y = int(offset_y + row * cell_size)
                x1 = max(0, int(offset_x))
                x2 = min(screen_width, int(offset_x + scaled_w))
                pygame.draw.line(screen, grid_color, (x1, y), (x2, y))

        if start_grid_point is not None:
            spx = int(offset_x + (start_grid_point[0] + 0.5) * cell_size)
            spy = int(offset_y + (start_grid_point[1] + 0.5) * cell_size)
            radius_pt = max(2, int(cell_size * 0.4))
            pygame.draw.circle(screen, (220, 50, 50), (spx, spy), radius_pt)

        cur_gx, cur_gy = screen_to_grid(mouse_pos[0], mouse_pos[1])
        coord_text = f"Grid: ({cur_gx}, {cur_gy}) | Zoom: {cell_size:.1f}x | Pan: Hold Right Click"
        coord_surf = info_font.render(coord_text, True, (80, 80, 80))
        screen.blit(coord_surf, (16, screen_height - 28))

        if current_time - toast_start_time < 2000:
            toast_surf = font.render(toast_message, True, (245, 245, 245))
            padding = 10
            toast_rect = toast_surf.get_rect(center=(screen_width // 2, 36))
            bg_rect = toast_rect.inflate(padding * 2, padding * 2)

            pygame.draw.rect(screen, (30, 30, 30), bg_rect, border_radius=6)
            screen.blit(toast_surf, toast_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
