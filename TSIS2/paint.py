import datetime
from pathlib import Path

import pygame

from tools import (
    calculate_rect,
    calculate_square,
    draw_rhombus,
    draw_right_triangle,
    draw_equilateral_triangle,
    draw_circle_by_points,
    flood_fill,
)

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (255, 255, 255)

BASE_DIR = Path(__file__).resolve().parent

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")
clock = pygame.time.Clock()

font_ui = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 16)
font_text = pygame.font.SysFont("Verdana", 28)

BLACK = (0, 0, 0)
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
thickness = 5

drawing = False
start_pos = None
prev_pos = None
current_pos = None

typing = False
text_input = ""
text_position = None

base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(BACKGROUND_COLOR)


def get_draw_color():
    if tool == "eraser":
        return BACKGROUND_COLOR
    return current_color


def save_canvas():
    assets_dir = BASE_DIR / "assets"
    assets_dir.mkdir(exist_ok=True)

    now = datetime.datetime.now()
    filename = assets_dir / f"canvas_{now.strftime('%Y%m%d_%H%M%S')}.png"

    pygame.image.save(base_layer, filename)
    print(f"Saved: {filename}")


def draw_ui():
    panel_rect = pygame.Rect(WIDTH - 255, 10, 240, 170)
    pygame.draw.rect(screen, (235, 235, 235), panel_rect)
    pygame.draw.rect(screen, BLACK, panel_rect, 2)

    tool_text = font_ui.render(f"Tool: {tool.upper()}", True, BLACK)
    brush_text = font_ui.render(f"Brush: {thickness}px", True, BLACK)
    color_text = font_ui.render(f"Color: {current_color_name}", True, BLACK)

    screen.blit(tool_text, (WIDTH - 240, 20))
    screen.blit(brush_text, (WIDTH - 240, 50))
    screen.blit(color_text, (WIDTH - 240, 80))

    outer_rect = pygame.Rect(WIDTH - 75, 78, 40, 40)
    inner_rect = pygame.Rect(WIDTH - 70, 83, 30, 30)

    pygame.draw.rect(screen, GRAY, outer_rect)
    pygame.draw.rect(screen, current_color, inner_rect)

    hint1 = font_small.render("W/L/R/C/E/S/T/F/D/B/X", True, BLACK)
    hint2 = font_small.render("A/G/H = brush size", True, BLACK)
    hint3 = font_small.render("Ctrl+S = save", True, BLACK)

    screen.blit(hint1, (WIDTH - 240, 120))
    screen.blit(hint2, (WIDTH - 240, 140))
    screen.blit(hint3, (WIDTH - 240, 158))


def finalize_shape():
    draw_color = get_draw_color()

    if tool == "line" and start_pos and current_pos:
        pygame.draw.line(base_layer, draw_color, start_pos, current_pos, thickness)

    elif tool == "rect" and start_pos and current_pos:
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


def draw_shape_preview():
    draw_color = get_draw_color()

    if tool == "line":
        pygame.draw.line(screen, draw_color, start_pos, current_pos, thickness)

    elif tool == "rect":
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


shape_tools = (
    "line",
    "rect",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus",
)

print("--- TSIS2 Paint Controls ---")
print("W - Pen")
print("L - Line")
print("R - Rectangle")
print("C - Circle")
print("E - Eraser")
print("S - Square")
print("T - Right triangle")
print("F - Equilateral triangle")
print("D - Rhombus")
print("B - Flood fill")
print("X - Text")
print("A - Small brush 2px")
print("G - Medium brush 5px")
print("H - Large brush 10px")
print("0-9 - Colors")
print("SPACE - Clear canvas")
print("Ctrl + S - Save canvas")
print("Enter - Confirm text")
print("Escape - Cancel text")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if typing:
                if event.key == pygame.K_RETURN:
                    text_surface = font_text.render(text_input, True, current_color)
                    base_layer.blit(text_surface, text_position)
                    typing = False
                    text_input = ""
                    text_position = None

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_input = ""
                    text_position = None

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

            else:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_canvas()

                elif event.key == pygame.K_w:
                    tool = "pen"
                    print("Tool: pen")

                elif event.key == pygame.K_l:
                    tool = "line"
                    print("Tool: line")

                elif event.key == pygame.K_r:
                    tool = "rect"
                    print("Tool: rectangle")

                elif event.key == pygame.K_c:
                    tool = "circle"
                    print("Tool: circle")

                elif event.key == pygame.K_e:
                    tool = "eraser"
                    print("Tool: eraser")

                elif event.key == pygame.K_s:
                    tool = "square"
                    print("Tool: square")

                elif event.key == pygame.K_t:
                    tool = "right_triangle"
                    print("Tool: right triangle")

                elif event.key == pygame.K_f:
                    tool = "equilateral_triangle"
                    print("Tool: equilateral triangle")

                elif event.key == pygame.K_d:
                    tool = "rhombus"
                    print("Tool: rhombus")

                elif event.key == pygame.K_b:
                    tool = "fill"
                    print("Tool: flood fill")

                elif event.key == pygame.K_x:
                    tool = "text"
                    print("Tool: text")

                elif event.key == pygame.K_a:
                    thickness = 2
                    print("Brush size: small 2px")

                elif event.key == pygame.K_g:
                    thickness = 5
                    print("Brush size: medium 5px")

                elif event.key == pygame.K_h:
                    thickness = 10
                    print("Brush size: large 10px")

                elif event.key == pygame.K_SPACE:
                    base_layer.fill(BACKGROUND_COLOR)
                    print("Canvas cleared")

                elif event.key in color_map:
                    current_color = color_map[event.key]
                    current_color_name = color_name_map[event.key]
                    print(f"Color: {current_color_name}")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if tool == "fill":
                    flood_fill(base_layer, event.pos, current_color)

                elif tool == "text":
                    typing = True
                    text_input = ""
                    text_position = event.pos

                else:
                    drawing = True
                    start_pos = event.pos
                    prev_pos = event.pos
                    current_pos = event.pos

                    if tool in ("pen", "eraser"):
                        pygame.draw.circle(
                            base_layer,
                            get_draw_color(),
                            event.pos,
                            max(1, thickness // 2),
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
                        thickness,
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
        draw_shape_preview()

    if typing and text_position:
        text_surface = font_text.render(text_input, True, current_color)
        screen.blit(text_surface, text_position)

    draw_ui()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()