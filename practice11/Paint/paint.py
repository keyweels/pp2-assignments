import math
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Practice 11")

clock = pygame.time.Clock()

font_ui = pygame.font.SysFont("Verdana", 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 105, 180)
BROWN = (139, 69, 19)

color_map = {
    pygame.K_0: BLACK,
    pygame.K_1: RED,
    pygame.K_2: GREEN,
    pygame.K_3: BLUE,
    pygame.K_4: YELLOW,
    pygame.K_5: ORANGE,
    pygame.K_6: PURPLE,
    pygame.K_7: PINK,
    pygame.K_8: BROWN,
    pygame.K_9: GRAY,
}

color_name_map = {
    pygame.K_0: "BLACK",
    pygame.K_1: "RED",
    pygame.K_2: "GREEN",
    pygame.K_3: "BLUE",
    pygame.K_4: "YELLOW",
    pygame.K_5: "ORANGE",
    pygame.K_6: "PURPLE",
    pygame.K_7: "PINK",
    pygame.K_8: "BROWN",
    pygame.K_9: "GRAY",
}

tool = "pen"
current_color = BLACK
current_color_name = "BLACK"
thickness = 4

drawing = False
start_pos = None
prev_pos = None
current_pos = None

base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(BACKGROUND_COLOR)


def calculate_rect(start, end):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return pygame.Rect(left, top, width, height)


def calculate_square(start, end):
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        left = x1 - side
    else:
        left = x1

    if y2 < y1:
        top = y1 - side
    else:
        top = y1

    return pygame.Rect(left, top, side, side)


def draw_circle_by_points(surface, color, start, end, width=0):
    cx, cy = start
    ex, ey = end

    radius = int(math.hypot(ex - cx, ey - cy))

    if radius > 0:
        pygame.draw.circle(surface, color, (cx, cy), radius, width)


def draw_right_triangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start, end, width):
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)
    height = int(side * math.sqrt(3) / 2)

    if x2 < x1:
        left = x1 - side
        right = x1
    else:
        left = x1
        right = x1 + side

    if y2 < y1:
        top = y1 - height
        bottom = y1
    else:
        top = y1
        bottom = y1 + height

    points = [
        ((left + right) // 2, top),
        (left, bottom),
        (right, bottom)
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, color, start, end, width):
    rect = calculate_rect(start, end)

    center_x = rect.centerx
    center_y = rect.centery

    points = [
        (center_x, rect.top),
        (rect.right, center_y),
        (center_x, rect.bottom),
        (rect.left, center_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


def get_draw_color():
    if tool == "eraser":
        return BACKGROUND_COLOR
    return current_color


def draw_ui():
    panel_rect = pygame.Rect(WIDTH - 250, 10, 230, 140)
    pygame.draw.rect(screen, (235, 235, 235), panel_rect)
    pygame.draw.rect(screen, BLACK, panel_rect, 2)

    tool_text = font_ui.render(f"Tool: {tool.upper()}", True, BLACK)
    screen.blit(tool_text, (WIDTH - 235, 20))

    thick_text = font_ui.render(f"Thickness: {thickness}", True, BLACK)
    screen.blit(thick_text, (WIDTH - 235, 50))

    color_text = font_ui.render(f"Color: {current_color_name}", True, BLACK)
    screen.blit(color_text, (WIDTH - 235, 80))

    outer_rect = pygame.Rect(WIDTH - 70, 105, 40, 40)
    inner_rect = pygame.Rect(WIDTH - 65, 110, 30, 30)

    pygame.draw.rect(screen, GRAY, outer_rect)
    pygame.draw.rect(screen, current_color, inner_rect)


def finalize_shape():
    draw_color = get_draw_color()

    if tool == "rect" and start_pos and current_pos:
        rect = calculate_rect(start_pos, current_pos)
        pygame.draw.rect(base_layer, draw_color, rect, thickness)

    elif tool == "square" and start_pos and current_pos:
        rect = calculate_square(start_pos, current_pos)
        pygame.draw.rect(base_layer, draw_color, rect, thickness)

    elif tool == "circle" and start_pos and current_pos:
        draw_circle_by_points(base_layer, draw_color, start_pos, current_pos, thickness)

    elif tool == "right_triangle" and start_pos and current_pos:
        draw_right_triangle(base_layer, draw_color, start_pos, current_pos, thickness)

    elif tool == "equilateral_triangle" and start_pos and current_pos:
        draw_equilateral_triangle(base_layer, draw_color, start_pos, current_pos, thickness)

    elif tool == "rhombus" and start_pos and current_pos:
        draw_rhombus(base_layer, draw_color, start_pos, current_pos, thickness)


shape_tools = (
    "rect",
    "square",
    "circle",
    "right_triangle",
    "equilateral_triangle",
    "rhombus"
)

print("--- Instructions ---")
print("W - Pen")
print("R - Rectangle")
print("S - Square")
print("C - Circle")
print("T - Right Triangle")
print("F - Equilateral Triangle")
print("D - Rhombus")
print("E - Eraser")
print("+ - Increase thickness")
print("- - Decrease thickness")
print("SPACE - Clear canvas")
print("0-9 - Change color")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                tool = "pen"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_s:
                tool = "square"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_t:
                tool = "right_triangle"
            elif event.key == pygame.K_f:
                tool = "equilateral_triangle"
            elif event.key == pygame.K_d:
                tool = "rhombus"
            elif event.key == pygame.K_e:
                tool = "eraser"

            elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                thickness += 1

            elif event.key == pygame.K_MINUS:
                if thickness > 1:
                    thickness -= 1

            elif event.key == pygame.K_SPACE:
                base_layer.fill(BACKGROUND_COLOR)

            elif event.key in color_map:
                current_color = color_map[event.key]
                current_color_name = color_name_map[event.key]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = event.pos
                prev_pos = event.pos
                current_pos = event.pos

                if tool in ("pen", "eraser"):
                    pygame.draw.circle(
                        base_layer,
                        get_draw_color(),
                        event.pos,
                        max(1, thickness // 2)
                    )

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = event.pos

                if tool in ("pen", "eraser"):
                    pygame.draw.line(
                        base_layer,
                        get_draw_color(),
                        prev_pos,
                        current_pos,
                        thickness
                    )
                    prev_pos = current_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if drawing:
                    current_pos = event.pos

                    if tool in shape_tools:
                        finalize_shape()

                drawing = False
                start_pos = None
                prev_pos = None
                current_pos = None

    screen.blit(base_layer, (0, 0))

    if drawing and tool in shape_tools and start_pos and current_pos:
        draw_color = get_draw_color()

        if tool == "rect":
            rect = calculate_rect(start_pos, current_pos)
            pygame.draw.rect(screen, draw_color, rect, thickness)

        elif tool == "square":
            rect = calculate_square(start_pos, current_pos)
            pygame.draw.rect(screen, draw_color, rect, thickness)

        elif tool == "circle":
            draw_circle_by_points(screen, draw_color, start_pos, current_pos, thickness)

        elif tool == "right_triangle":
            draw_right_triangle(screen, draw_color, start_pos, current_pos, thickness)

        elif tool == "equilateral_triangle":
            draw_equilateral_triangle(screen, draw_color, start_pos, current_pos, thickness)

        elif tool == "rhombus":
            draw_rhombus(screen, draw_color, start_pos, current_pos, thickness)

    draw_ui()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()