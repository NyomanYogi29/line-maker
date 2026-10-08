import pygame
import math
from algorithm import brute_force
from algorithm import dda
from algorithm import bresenham

ALGORITHMS = {
    1: "Brute Force - Garis",
    2: "DDA - Garis",
    3: "Bresenham - Garis",
    4: "Bresenham - Lingkaran"
}

ALGORITHM_MODES = {
    pygame.K_1: ALGORITHMS[1],                                                                                                                       
    pygame.K_2: ALGORITHMS[2],                                                                                                                       
    pygame.K_3: ALGORITHMS[3],                                                                                                                       
    pygame.K_4: ALGORITHMS[4],  
}

def main() -> None:
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Line Maker - Algoritma Garis")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()

    bg_color = (255, 255, 255)
    line_color = (20, 20, 20)

    canvas = pygame.Surface((screen_width, screen_height))
    canvas.fill(bg_color)

    current_mode = ALGORITHMS[1]
    toast_message = current_mode
    toast_start_time = pygame.time.get_ticks()

    start_point: tuple[int, int] | None = None
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in ALGORITHM_MODES:
                    current_mode = ALGORITHM_MODES[event.key]
                    toast_message = f"Mode: {current_mode}"
                    toast_start_time = current_time
                    start_point = None
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_point is None:
                    start_point = event.pos
                    print(f"[{current_mode}], starting point: {start_point}")
                else:
                    end_point = event.pos
                    pixels:  list[tuple[int, int]] = []
                    print(f"[{current_mode}], ending point: {end_point}")
                    if current_mode == ALGORITHMS[1]:
                        pixels = brute_force.brute_force(start_point[0], end_point[0], start_point[1], end_point[1])
                    elif current_mode == ALGORITHMS[2]:
                        pixels = dda.DDA(start_point[0], end_point[0], start_point[1], end_point[1])
                    elif current_mode == ALGORITHMS[3]:
                        pixels = bresenham.line(start_point[0], end_point[0], start_point[1], end_point[1])
                    elif current_mode == ALGORITHMS[4]:
                        dx = end_point[0] - start_point[0]
                        dy = end_point[1] - start_point[1]

                        radius = round(math.hypot(dx, dy))

                        pixels = bresenham.circle(start_point[0], start_point[1], radius)
                    if pixels:
                        print(f"Total pixels: {len(pixels)}")
                    
                    for px, py in pixels:
                        if 0 <= px < screen_width and 0 <= py < screen_height:
                            canvas.set_at((px, py), (line_color))
                    start_point = None

        screen.blit(canvas, (0, 0))

        if current_time - toast_start_time < 2000:
            toast_surf = font.render(toast_message, True, (240, 240, 240))
            padding = 10
            toast_rect = toast_surf.get_rect(center=(screen_width // 2, 40))
            bg_rect = toast_rect.inflate(padding * 2, padding * 2)

            pygame.draw.rect(screen, (40, 40, 40), bg_rect, border_radius=6)
            screen.blit(toast_surf, toast_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
