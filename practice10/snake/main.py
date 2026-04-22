import pygame
import random
import math

pygame.init()

WIDTH = 720
HEIGHT = 760
CELL = 24
GRID_WIDTH = WIDTH // CELL
GRID_HEIGHT = 28
PLAY_HEIGHT = GRID_HEIGHT * CELL
HUD_HEIGHT = HEIGHT - PLAY_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake")
clock = pygame.time.Clock()

BG_TOP = (10, 14, 22)
BG_BOTTOM = (18, 24, 38)
PANEL = (20, 24, 34)
GRID_A = (18, 24, 34)
GRID_B = (22, 28, 40)
WALL = (80, 90, 110)
WALL_GLOW = (130, 140, 170)
SNAKE_HEAD = (0, 255, 170)
SNAKE_BODY = (0, 185, 125)
SNAKE_ACCENT = (180, 255, 220)
FOOD_RED = (255, 90, 110)
FOOD_GLOW = (255, 160, 180)
WHITE = (245, 248, 255)
SOFT = (170, 180, 200)
YELLOW = (255, 220, 120)
CYAN = (80, 220, 255)
RED = (255, 95, 95)
BLACK = (16, 18, 24)

title_font = pygame.font.SysFont("Arial", 44, bold=True)
big_font = pygame.font.SysFont("Arial", 30, bold=True)
font = pygame.font.SysFont("Arial", 24, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

particles = []


def cell_to_pixel(pos):
    return pos[0] * CELL, pos[1] * CELL


def draw_vertical_gradient(surface, top, bottom):
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_glow(surface, center, radius, color, alpha):
    glow = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*color, alpha), (radius * 2, radius * 2), radius)
    pygame.draw.circle(glow, (*color, alpha // 2), (radius * 2, radius * 2), int(radius * 1.4))
    surface.blit(glow, (center[0] - radius * 2, center[1] - radius * 2))


def create_border_walls():
    walls = set()
    for x in range(GRID_WIDTH):
        walls.add((x, 0))
        walls.add((x, GRID_HEIGHT - 1))
    for y in range(GRID_HEIGHT):
        walls.add((0, y))
        walls.add((GRID_WIDTH - 1, y))
    return walls


def random_food(snake, walls):
    while True:
        pos = (
            random.randint(1, GRID_WIDTH - 2),
            random.randint(1, GRID_HEIGHT - 2)
        )
        if pos not in snake and pos not in walls:
            return pos


def spawn_particles(cell_pos, color):
    px, py = cell_to_pixel(cell_pos)
    cx = px + CELL // 2
    cy = py + CELL // 2
    for _ in range(16):
        particles.append({
            "x": cx,
            "y": cy,
            "dx": random.uniform(-2.5, 2.5),
            "dy": random.uniform(-2.5, 2.5),
            "life": random.randint(16, 28),
            "color": color,
            "size": random.randint(2, 5),
        })


def update_particles():
    for p in particles[:]:
        p["x"] += p["dx"]
        p["y"] += p["dy"]
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)


def draw_particles():
    for p in particles:
        alpha = max(0, min(255, p["life"] * 10))
        surf = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*p["color"], alpha), (p["size"], p["size"]), p["size"])
        screen.blit(surf, (p["x"] - p["size"], p["y"] - p["size"]))


def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = GRID_A if (x + y) % 2 == 0 else GRID_B
            pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))

    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (26, 34, 48), (x, 0), (x, PLAY_HEIGHT), 1)
    for y in range(0, PLAY_HEIGHT, CELL):
        pygame.draw.line(screen, (26, 34, 48), (0, y), (WIDTH, y), 1)


def draw_walls(walls):
    for wall in walls:
        x, y = cell_to_pixel(wall)
        draw_glow(screen, (x + CELL // 2, y + CELL // 2), 12, WALL_GLOW, 26)
        draw_rounded_rect(screen, WALL, (x + 2, y + 2, CELL - 4, CELL - 4), 6)


def draw_snake(snake, direction):
    for i, segment in enumerate(snake):
        x, y = cell_to_pixel(segment)

        if i == 0:
            draw_glow(screen, (x + CELL // 2, y + CELL // 2), 14, (0, 255, 170), 30)
            draw_rounded_rect(screen, SNAKE_HEAD, (x + 2, y + 2, CELL - 4, CELL - 4), 8)

            eye_size = 3
            if direction == (1, 0):
                eyes = [(x + 16, y + 8), (x + 16, y + 16)]
            elif direction == (-1, 0):
                eyes = [(x + 8, y + 8), (x + 8, y + 16)]
            elif direction == (0, -1):
                eyes = [(x + 8, y + 8), (x + 16, y + 8)]
            else:
                eyes = [(x + 8, y + 16), (x + 16, y + 16)]

            for ex, ey in eyes:
                pygame.draw.circle(screen, BLACK, (ex, ey), eye_size)
        else:
            ratio = max(0.55, 1 - i * 0.02)
            color = (
                int(SNAKE_BODY[0] * ratio),
                int(SNAKE_BODY[1] * ratio),
                int(SNAKE_BODY[2] * ratio),
            )
            draw_rounded_rect(screen, color, (x + 3, y + 3, CELL - 6, CELL - 6), 7)
            if i % 2 == 0:
                pygame.draw.rect(screen, SNAKE_ACCENT, (x + 7, y + 9, CELL - 14, 4), border_radius=2)


def draw_food(food_pos, ticks):
    x, y = cell_to_pixel(food_pos)
    pulse = 1 + 0.08 * math.sin(ticks / 180)
    radius = int(11 * pulse)

    draw_glow(screen, (x + CELL // 2, y + CELL // 2), 18, FOOD_GLOW, 30)
    pygame.draw.circle(screen, FOOD_RED, (x + CELL // 2, y + CELL // 2), radius)
    pygame.draw.circle(screen, (255, 180, 190), (x + CELL // 2 - 3, y + CELL // 2 - 3), max(4, radius - 6))


def draw_hud(score, level, speed, foods, best_score):
    panel = pygame.Surface((WIDTH, HUD_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(panel, (18, 22, 34, 240), (0, 0, WIDTH, HUD_HEIGHT))
    pygame.draw.line(panel, (40, 48, 66), (0, 0), (WIDTH, 0), 2)
    screen.blit(panel, (0, PLAY_HEIGHT))

    title = big_font.render("NEON SNAKE", True, WHITE)
    score_text = font.render(f"Score: {score}", True, CYAN)
    level_text = font.render(f"Level: {level}", True, WHITE)
    speed_text = font.render(f"Speed: {speed}", True, WHITE)
    foods_text = small_font.render(f"Foods: {foods}", True, SOFT)
    best_text = small_font.render(f"Best: {best_score}", True, YELLOW)
    help_text = small_font.render("Arrows to move   |   R to restart after game over", True, SOFT)

    screen.blit(title, (22, PLAY_HEIGHT + 12))
    screen.blit(score_text, (24, PLAY_HEIGHT + 58))
    screen.blit(level_text, (190, PLAY_HEIGHT + 58))
    screen.blit(speed_text, (330, PLAY_HEIGHT + 58))
    screen.blit(foods_text, (470, PLAY_HEIGHT + 61))
    screen.blit(best_text, (610, PLAY_HEIGHT + 61))
    screen.blit(help_text, (24, PLAY_HEIGHT + 95))


def draw_start_screen():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 110))
    screen.blit(overlay, (0, 0))

    card = pygame.Surface((450, 250), pygame.SRCALPHA)
    pygame.draw.rect(card, (18, 22, 34, 235), (0, 0, 450, 250), border_radius=24)
    pygame.draw.rect(card, (0, 255, 170, 45), (0, 0, 450, 250), 1, border_radius=24)
    screen.blit(card, (135, 180))

    title = title_font.render("NEON SNAKE", True, WHITE)
    line1 = font.render("Collect food, avoid walls and yourself", True, SOFT)
    line2 = font.render("Every 4 foods = next level and more speed", True, SOFT)
    line3 = small_font.render("Press SPACE to start", True, YELLOW)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, 240)))
    screen.blit(line1, line1.get_rect(center=(WIDTH // 2, 310)))
    screen.blit(line2, line2.get_rect(center=(WIDTH // 2, 350)))
    screen.blit(line3, line3.get_rect(center=(WIDTH // 2, 395)))


def draw_countdown(value):
    overlay = pygame.Surface((WIDTH, PLAY_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 60))
    screen.blit(overlay, (0, 0))

    text = title_font.render(str(value), True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, PLAY_HEIGHT // 2)))


def draw_game_over(score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 130))
    screen.blit(overlay, (0, 0))

    card = pygame.Surface((400, 220), pygame.SRCALPHA)
    pygame.draw.rect(card, (18, 22, 34, 240), (0, 0, 400, 220), border_radius=24)
    pygame.draw.rect(card, (255, 95, 95, 45), (0, 0, 400, 220), 1, border_radius=24)
    screen.blit(card, (160, 200))

    title = title_font.render("GAME OVER", True, RED)
    result = big_font.render(f"Final score: {score}", True, WHITE)
    restart = font.render("Press R to restart", True, YELLOW)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, 260)))
    screen.blit(result, result.get_rect(center=(WIDTH // 2, 325)))
    screen.blit(restart, restart.get_rect(center=(WIDTH // 2, 385)))


def reset_game():
    global snake, direction, next_direction, food, score, level, foods_eaten, speed, game_over
    global started, countdown_active, countdown_value, countdown_time

    snake = [(12, 12), (11, 12), (10, 12)]
    direction = (1, 0)
    next_direction = (1, 0)
    score = 0
    level = 1
    foods_eaten = 0
    speed = 8
    game_over = False
    started = False
    countdown_active = False
    countdown_value = 3
    countdown_time = 0
    food = random_food(snake, walls)


walls = create_border_walls()
best_score = 0
reset_game()

MOVE_EVENT = pygame.USEREVENT + 1


def update_move_timer():
    interval = max(65, int(170 - (speed - 8) * 8))
    pygame.time.set_timer(MOVE_EVENT, interval)


update_move_timer()

running = True
while running:
    ticks = pygame.time.get_ticks()
    update_particles()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if not started and not game_over:
                if event.key == pygame.K_SPACE:
                    started = True
                    countdown_active = True
                    countdown_value = 3
                    countdown_time = ticks

            elif game_over:
                if event.key == pygame.K_r:
                    reset_game()
                    update_move_timer()

            else:
                if event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)
                elif event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)

        elif event.type == MOVE_EVENT:
            if started and not countdown_active and not game_over:
                direction = next_direction
                head_x, head_y = snake[0]
                new_head = (head_x + direction[0], head_y + direction[1])

                if new_head in walls or new_head in snake:
                    game_over = True
                    best_score = max(best_score, score)
                    spawn_particles(snake[0], (255, 95, 95))
                else:
                    snake.insert(0, new_head)

                    if new_head == food:
                        score += 1
                        foods_eaten += 1
                        spawn_particles(food, (255, 220, 120))
                        food = random_food(snake, walls)

                        if foods_eaten % 4 == 0:
                            level += 1
                            speed += 1
                            update_move_timer()
                    else:
                        snake.pop()

    if countdown_active and ticks - countdown_time >= 1000:
        countdown_value -= 1
        countdown_time = ticks
        if countdown_value <= 0:
            countdown_active = False

    draw_vertical_gradient(screen, BG_TOP, BG_BOTTOM)
    draw_grid()
    draw_walls(walls)
    draw_food(food, ticks)
    draw_snake(snake, direction)
    draw_particles()
    draw_hud(score, level, speed, foods_eaten, best_score)

    if not started and not game_over:
        draw_start_screen()
    elif countdown_active:
        draw_countdown(countdown_value)
    elif game_over:
        draw_game_over(score)

    pygame.display.flip()

pygame.quit()