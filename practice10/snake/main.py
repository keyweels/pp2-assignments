import pygame
import random
import sys

pygame.init()

# -----------------------------
# GAME SETTINGS
# -----------------------------
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20
FPS = 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# -----------------------------
# COLORS
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
GRAY = (200, 200, 200)

# -----------------------------
# FONTS
# -----------------------------
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 42)

# -----------------------------
# GRID SETTINGS
# -----------------------------
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE


# -----------------------------
# FUNCTION TO DRAW TEXT
# -----------------------------
def draw_text(text, font_obj, color, x, y):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))


# -----------------------------
# FUNCTION TO CREATE SAFE FOOD
# -----------------------------
def generate_food(snake, walls):
    while True:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        position = (x, y)

        if position not in snake and position not in walls:

            value = random.choice([1, 2, 3])

            if value == 1:
                color = RED
            elif value == 2:
                color = BLUE
            else:
                color = GRAY

            # Time when food was created
            spawn_time = pygame.time.get_ticks()

            lifetime = 5000

            return {
                "position": position,
                "value": value,
                "color": color,
                "spawn_time": spawn_time,
                "lifetime": lifetime
            }


# -----------------------------
# WALLS
# -----------------------------
walls = {
    (10, 10), (11, 10), (12, 10), (13, 10),
    (18, 15), (18, 16), (18, 17), (18, 18),
    (5, 20), (6, 20), (7, 20), (8, 20)
}

# -----------------------------
# SNAKE START SETTINGS
# -----------------------------
snake = [(5, 5), (4, 5), (3, 5)]
direction = (1, 0)
next_direction = direction

food = generate_food(snake, walls)

score = 0
level = 1
foods_eaten = 0
speed = FPS

running = True
game_over = False

# -----------------------------
# MAIN GAME LOOP
# -----------------------------
while running:
    clock.tick(speed)

    # -----------------------------
    # HANDLE EVENTS
    # -----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Change direction with arrow keys
            if event.key == pygame.K_UP and direction != (0, 1):
                next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                next_direction = (1, 0)

            # Restart after game over
            if game_over and event.key == pygame.K_r:
                snake = [(5, 5), (4, 5), (3, 5)]
                direction = (1, 0)
                next_direction = direction
                food = generate_food(snake, walls)
                score = 0
                level = 1
                foods_eaten = 0
                speed = FPS
                game_over = False

    if not game_over:
        # Update direction
        direction = next_direction

        # -----------------------------
        # MOVE SNAKE
        # -----------------------------
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # -----------------------------
        # CHECK BORDER COLLISION
        # -----------------------------
        if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
            game_over = True

        # -----------------------------
        # CHECK WALL COLLISION
        # -----------------------------
        elif new_head in walls:
            game_over = True

        # -----------------------------
        # CHECK SELF COLLISION
        # -----------------------------
        elif new_head in snake:
            game_over = True

        else:
            # Add new head
            snake.insert(0, new_head)

            # -----------------------------
            # CHECK FOOD
            if new_head == food["position"]:
                # Add score based on food weight
                score += food["value"]
                foods_eaten += 1

                # Generate new food
                food = generate_food(snake, walls)

                # Increase level every 4 foods
                if foods_eaten % 4 == 0:
                    level += 1
                    speed += 2
            else:
                # Remove tail if food was not eaten
                snake.pop()

    # -----------------------------
    # DRAW EVERYTHING
    # -----------------------------
    screen.fill(WHITE)

    # Draw grid
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Draw walls
    for wall in walls:
        wx, wy = wall
        pygame.draw.rect(
            screen,
            BLACK,
            (wx * CELL_SIZE, wy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    # Draw snake
    for i, segment in enumerate(snake):
        sx, sy = segment

        if i == 0:
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                (sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
        else:
            pygame.draw.rect(
                screen,
                GREEN,
                (sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

    # Draw food
    fx, fy = food["position"]
    pygame.draw.rect(
        screen,
        food["color"],
        (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )

    # Draw score and level
    draw_text(f"Score: {score}", font, BLUE, 10, 10)
    draw_text(f"Level: {level}", font, BLUE, 10, 40)
    draw_text(f"Food value: {food['value']}", font, BLACK, 10, 70)

    time_left = max(0, (food["lifetime"] - (pygame.time.get_ticks() - food["spawn_time"])) // 1000)
    draw_text(f"Food timer: {time_left}", font, BLACK, 10, 100)
    # Draw game over text
    if game_over:
        draw_text("GAME OVER", big_font, RED, WIDTH // 2 - 120, HEIGHT // 2 - 40)
        draw_text("Press R to restart", font, BLACK, WIDTH // 2 - 105, HEIGHT // 2 + 20)

    pygame.display.update()

pygame.quit()
sys.exit()