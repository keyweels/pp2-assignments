import json
import random
from pathlib import Path

import pygame

from db import get_personal_best, save_result


WIDTH = 600
HEIGHT = 600
CELL = 30
GRID_W = WIDTH // CELL
GRID_H = HEIGHT // CELL

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (120, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 220, 0)
BLUE = (0, 100, 255)
PURPLE = (160, 0, 200)
ORANGE = (255, 140, 0)

SETTINGS_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "snake_color": [255, 0, 0],
    "grid": True,
    "sound": True
}


def load_settings():
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        settings = json.load(file)

    for key in DEFAULT_SETTINGS:
        if key not in settings:
            settings[key] = DEFAULT_SETTINGS[key]

    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def same_pos(a, b):
    return a.x == b.x and a.y == b.y


def point_in_list(point, points):
    for item in points:
        if item.x == point.x and item.y == point.y:
            return True
    return False


def random_free_point(snake, obstacles, extra_points=None):
    if extra_points is None:
        extra_points = []

    while True:
        point = Point(random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))

        if point_in_list(point, snake.body):
            continue

        if point_in_list(point, obstacles):
            continue

        if point_in_list(point, extra_points):
            continue

        return point


class Snake:
    def __init__(self, color):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.food_count = 0
        self.level = 1
        self.color = color
        self.shield = False

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def border_collision(self):
        head = self.body[0]
        return head.x < 0 or head.x >= GRID_W or head.y < 0 or head.y >= GRID_H

    def self_collision(self):
        head = self.body[0]

        for segment in self.body[1:]:
            if same_pos(head, segment):
                return True

        return False

    def obstacle_collision(self, obstacles):
        return point_in_list(self.body[0], obstacles)

    def grow(self):
        head = self.body[0]
        self.body.append(Point(head.x, head.y))

    def shorten(self, amount):
        for _ in range(amount):
            if len(self.body) > 1:
                self.body.pop()

    def draw(self, screen):
        head = self.body[0]
        pygame.draw.rect(screen, self.color, (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, YELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))


class Food:
    def __init__(self, snake, obstacles, extra_points=None):
        self.pos = random_free_point(snake, obstacles, extra_points)
        self.weight = random.choice([1, 2, 3])
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 6000

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.life_time

    def draw(self, screen):
        if self.weight == 1:
            color = GREEN
        elif self.weight == 2:
            color = ORANGE
        else:
            color = PURPLE

        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))


class PoisonFood:
    def __init__(self, snake, obstacles, extra_points=None):
        self.pos = random_free_point(snake, obstacles, extra_points)
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 8000

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.life_time

    def draw(self, screen):
        pygame.draw.rect(screen, DARK_RED, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))


class PowerUp:
    def __init__(self):
        self.kind = None
        self.pos = Point(0, 0)
        self.spawn_time = 0
        self.life_time = 8000
        self.active_on_field = False

    def spawn(self, snake, obstacles, extra_points):
        if self.active_on_field:
            return

        self.kind = random.choice(["speed", "slow", "shield"])
        self.pos = random_free_point(snake, obstacles, extra_points)
        self.spawn_time = pygame.time.get_ticks()
        self.active_on_field = True

    def expired(self):
        return self.active_on_field and pygame.time.get_ticks() - self.spawn_time > self.life_time

    def collect(self):
        self.active_on_field = False
        return self.kind

    def draw(self, screen):
        if not self.active_on_field:
            return

        if self.kind == "speed":
            color = BLUE
            label = "S"
        elif self.kind == "slow":
            color = PURPLE
            label = "L"
        else:
            color = ORANGE
            label = "H"

        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

        font = pygame.font.SysFont("Verdana", 16, bold=True)
        text = font.render(label, True, WHITE)
        rect = text.get_rect(center=(self.pos.x * CELL + CELL // 2, self.pos.y * CELL + CELL // 2))
        screen.blit(text, rect)


def draw_grid_chess(screen):
    colors = [WHITE, GRAY]

    for i in range(GRID_W):
        for j in range(GRID_H):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))


def draw_grid_lines(screen):
    for i in range(GRID_W):
        for j in range(GRID_H):
            pygame.draw.rect(screen, GRAY, (i * CELL, j * CELL, CELL, CELL), 1)


def draw_obstacles(screen, obstacles):
    for block in obstacles:
        pygame.draw.rect(screen, BLACK, (block.x * CELL, block.y * CELL, CELL, CELL))


def generate_obstacles(snake, level):
    if level < 3:
        return []

    obstacles = []
    count = min(4 + level, 12)

    forbidden = []
    head = snake.body[0]

    # Keep free area around the snake head.
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            forbidden.append(Point(head.x + dx, head.y + dy))

    tries = 0
    while len(obstacles) < count and tries < 300:
        tries += 1
        point = Point(random.randint(1, GRID_W - 2), random.randint(1, GRID_H - 2))

        if point_in_list(point, snake.body):
            continue

        if point_in_list(point, forbidden):
            continue

        if point_in_list(point, obstacles):
            continue

        obstacles.append(point)

    return obstacles


def run_game(screen, username, settings):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 18)

    snake = Snake(tuple(settings["snake_color"]))
    personal_best = get_personal_best(username)

    obstacles = []
    food = Food(snake, obstacles)
    poison = PoisonFood(snake, obstacles, [food.pos])
    powerup = PowerUp()

    running = True
    game_over = False

    active_power = None
    power_end = 0
    last_power_spawn = pygame.time.get_ticks()

    while running:
        now = pygame.time.get_ticks()

        base_fps = 5 + snake.level

        if active_power == "speed":
            fps = base_fps + 5
            if now > power_end:
                active_power = None

        elif active_power == "slow":
            fps = max(3, base_fps - 3)
            if now > power_end:
                active_power = None

        else:
            fps = base_fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx = 1
                    snake.dy = 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx = -1
                    snake.dy = 0
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx = 0
                    snake.dy = 1
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx = 0
                    snake.dy = -1

        snake.move()

        collision = snake.border_collision() or snake.self_collision() or snake.obstacle_collision(obstacles)

        if collision:
            if snake.shield:
                snake.shield = False
                snake.body[0].x = GRID_W // 2
                snake.body[0].y = GRID_H // 2
            else:
                game_over = True
                running = False

        if not game_over:
            head = snake.body[0]

            if same_pos(head, food.pos):
                snake.grow()
                snake.score += food.weight
                snake.food_count += 1

                old_level = snake.level
                snake.level = snake.food_count // 4 + 1

                if snake.level != old_level:
                    obstacles = generate_obstacles(snake, snake.level)

                food = Food(snake, obstacles, [poison.pos])

            if food.expired():
                food = Food(snake, obstacles, [poison.pos])

            if same_pos(head, poison.pos):
                snake.shorten(2)

                if len(snake.body) <= 1:
                    game_over = True
                    running = False
                else:
                    poison = PoisonFood(snake, obstacles, [food.pos])

            if poison.expired():
                poison = PoisonFood(snake, obstacles, [food.pos])

            if not powerup.active_on_field and now - last_power_spawn > 9000:
                powerup.spawn(snake, obstacles, [food.pos, poison.pos])
                last_power_spawn = now

            if powerup.expired():
                powerup.active_on_field = False

            if powerup.active_on_field and same_pos(head, powerup.pos):
                kind = powerup.collect()

                if kind == "speed":
                    active_power = "speed"
                    power_end = now + 5000

                elif kind == "slow":
                    active_power = "slow"
                    power_end = now + 5000

                elif kind == "shield":
                    snake.shield = True

        draw_grid_chess(screen)

        if settings["grid"]:
            draw_grid_lines(screen)

        draw_obstacles(screen, obstacles)
        food.draw(screen)
        poison.draw(screen)
        powerup.draw(screen)
        snake.draw(screen)

        screen.blit(font.render(f"Score: {snake.score}", True, BLACK), (10, 10))
        screen.blit(font.render(f"Level: {snake.level}", True, BLACK), (10, 32))
        screen.blit(font.render(f"Best: {personal_best}", True, BLACK), (10, 54))
        screen.blit(font.render(f"Power: {active_power if active_power else 'None'}", True, BLACK), (10, 76))
        screen.blit(font.render(f"Shield: {'ON' if snake.shield else 'OFF'}", True, BLACK), (10, 98))

        pygame.display.flip()
        clock.tick(fps)

    save_result(username, snake.score, snake.level)

    result = {
        "score": snake.score,
        "level": snake.level,
        "best": max(personal_best, snake.score)
    }

    return "game_over", result
