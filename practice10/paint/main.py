import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Practice")

clock = pygame.time.Clock()

# -----------------------------
# COLORS
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 180, 0)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)

current_color = BLACK

# -----------------------------
# MODES
# -----------------------------
mode = "draw"  # draw, rect, circle, square, triangle, right_triangle, rhombus, eraser

drawing = False
start_pos = None

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# -----------------------------
# MAIN LOOP
# -----------------------------
running = True

while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -----------------------------
        # KEY CONTROLS
        # -----------------------------
        if event.type == pygame.KEYDOWN:

            # COLORS
            if event.key == pygame.K_1:
                current_color = BLACK
            if event.key == pygame.K_2:
                current_color = RED
            if event.key == pygame.K_3:
                current_color = GREEN
            if event.key == pygame.K_4:
                current_color = BLUE

            # MODES
            if event.key == pygame.K_d:
                mode = "draw"
            if event.key == pygame.K_r:
                mode = "rect"
            if event.key == pygame.K_c:
                mode = "circle"
            if event.key == pygame.K_s:
                mode = "square"
            if event.key == pygame.K_t:
                mode = "triangle"
            if event.key == pygame.K_y:
                mode = "right_triangle"
            if event.key == pygame.K_h:
                mode = "rhombus"
            if event.key == pygame.K_e:
                mode = "eraser"

        # -----------------------------
        # MOUSE EVENTS
        # -----------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x1, y1 = start_pos
            x2, y2 = end_pos

            # RECTANGLE
            if mode == "rect":
                pygame.draw.rect(canvas, current_color, (x1, y1, x2-x1, y2-y1), 2)

            # CIRCLE
            elif mode == "circle":
                radius = int(((x2-x1)**2 + (y2-y1)**2) ** 0.5)
                pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

            # SQUARE
            elif mode == "square":
                size = min(abs(x2-x1), abs(y2-y1))
                pygame.draw.rect(canvas, current_color, (x1, y1, size, size), 2)

            # RIGHT TRIANGLE
            elif mode == "right_triangle":
                points = [(x1, y1), (x2, y1), (x1, y2)]
                pygame.draw.polygon(canvas, current_color, points, 2)

            # EQUILATERAL TRIANGLE
            elif mode == "triangle":
                points = [(x1, y2), ((x1+x2)//2, y1), (x2, y2)]
                pygame.draw.polygon(canvas, current_color, points, 2)

            # RHOMBUS
            elif mode == "rhombus":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                points = [
                    (cx, y1),
                    (x2, cy),
                    (cx, y2),
                    (x1, cy)
                ]
                pygame.draw.polygon(canvas, current_color, points, 2)

        # FREE DRAW & ERASER
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "draw":
                pygame.draw.circle(canvas, current_color, event.pos, 5)
            elif mode == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, 10)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()