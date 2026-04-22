import pygame

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (200, 200, 200)
DARK = (40, 40, 40)

COLORS = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 200, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

current_color = BLACK
brush_size = 5
mode = "brush"  # brush, rect, circle, eraser

drawing = False
start_pos = None

font = pygame.font.SysFont("Arial", 20)


def draw_ui():
    pygame.draw.rect(screen, DARK, (0, 0, WIDTH, 50))

    # colors
    for i, c in enumerate(COLORS):
        pygame.draw.rect(screen, c, (10 + i * 40, 10, 30, 30))

    # tools
    text = font.render("B:Brush R:Rect C:Circle E:Eraser +/- Size X:Clear", True, (255, 255, 255))
    screen.blit(text, (350, 15))


running = True
while running:
    screen.blit(canvas, (0, 0))
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

            # choose color
            for i, c in enumerate(COLORS):
                rect = pygame.Rect(10 + i * 40, 10, 30, 30)
                if rect.collidepoint(event.pos):
                    current_color = c

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if mode == "rect" and start_pos:
                pygame.draw.rect(canvas, current_color, (*start_pos, event.pos[0]-start_pos[0], event.pos[1]-start_pos[1]), 2)

            if mode == "circle" and start_pos:
                radius = int(((event.pos[0]-start_pos[0])**2 + (event.pos[1]-start_pos[1])**2) ** 0.5)
                pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                mode = "brush"
            elif event.key == pygame.K_r:
                mode = "rect"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_e:
                mode = "eraser"
            elif event.key == pygame.K_EQUALS:
                brush_size += 2
            elif event.key == pygame.K_MINUS:
                brush_size = max(2, brush_size - 2)
            elif event.key == pygame.K_x:
                canvas.fill(WHITE)

    if drawing and mode == "brush":
        pygame.draw.circle(canvas, current_color, pygame.mouse.get_pos(), brush_size)

    if drawing and mode == "eraser":
        pygame.draw.circle(canvas, WHITE, pygame.mouse.get_pos(), brush_size)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()