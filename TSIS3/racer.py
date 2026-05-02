import random
import time
from pathlib import Path

import pygame

from persistence import add_score


WIDTH = 500
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
RED = (220, 0, 0)
BLUE = (0, 0, 220)
GREEN = (0, 180, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (130, 0, 130)
CYAN = (0, 200, 255)

LANES = [100, 200, 300, 400]
FINISH_DISTANCE = 3000
ASSET_DIR = Path("assets")

DIFFICULTY_DATA = {
    "easy": {
        "enemy_speed": 5,
        "traffic_delay": 1000,
        "obstacle_delay": 1600
    },
    "normal": {
        "enemy_speed": 7,
        "traffic_delay": 800,
        "obstacle_delay": 1200
    },
    "hard": {
        "enemy_speed": 9,
        "traffic_delay": 600,
        "obstacle_delay": 900
    }
}


def load_image(name, size=None):
    image = pygame.image.load(str(ASSET_DIR / name)).convert_alpha()

    if size:
        image = pygame.transform.scale(image, size)

    return image


def safe_lane(player_rect):
    safe_lanes = []

    for lane in LANES:
        if abs(lane - player_rect.centerx) > 70:
            safe_lanes.append(lane)

    if len(safe_lanes) == 0:
        safe_lanes = LANES[:]

    return random.choice(safe_lanes)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = load_image("Player.png", (50, 90))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 6

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)

        if self.rect.left < 35:
            self.rect.left = 35
        if self.rect.right > WIDTH - 35:
            self.rect.right = WIDTH - 35
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, player_rect, speed):
        super().__init__()

        self.image = load_image("Enemy.png", (50, 90))
        self.rect = self.image.get_rect()
        self.rect.centerx = safe_lane(player_rect)
        self.rect.bottom = -random.randint(40, 300)
        self.speed = speed

    def move(self, road_speed):
        self.rect.y += self.speed + road_speed // 3

        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()

        coin_data = random.choice([
            ("20tg.png", 20),
            ("50tg.png", 50),
            ("100tg.png", 100)
        ])

        self.filename = coin_data[0]
        self.value = coin_data[1]

        self.image = load_image(self.filename, (38, 38))
        self.rect = self.image.get_rect()
        self.rect.centerx = safe_lane(player_rect)
        self.rect.y = -random.randint(60, 450)
        self.speed = 4

    def move(self, road_speed):
        self.rect.y += self.speed + road_speed // 3

        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()

        self.kind = random.choice(["barrier", "oil", "pothole", "speed_bump"])
        self.image = pygame.Surface((65, 35), pygame.SRCALPHA)

        if self.kind == "barrier":
            pygame.draw.rect(self.image, ORANGE, (0, 0, 65, 35))
            pygame.draw.rect(self.image, BLACK, (0, 0, 65, 35), 2)

        elif self.kind == "oil":
            pygame.draw.ellipse(self.image, BLACK, (6, 7, 53, 22))

        elif self.kind == "pothole":
            pygame.draw.ellipse(self.image, GRAY, (5, 5, 55, 25))
            pygame.draw.ellipse(self.image, BLACK, (12, 9, 40, 16))

        elif self.kind == "speed_bump":
            pygame.draw.rect(self.image, YELLOW, (0, 12, 65, 12))
            pygame.draw.rect(self.image, BLACK, (0, 12, 65, 12), 1)

        self.rect = self.image.get_rect()
        self.rect.centerx = safe_lane(player_rect)
        self.rect.y = -random.randint(80, 500)
        self.speed = 5

    def move(self, road_speed):
        self.rect.y += self.speed + road_speed // 3

        if self.rect.top > HEIGHT:
            self.kill()


class MovingBarrier(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((90, 28), pygame.SRCALPHA)
        pygame.draw.rect(self.image, ORANGE, (0, 0, 90, 28))
        pygame.draw.rect(self.image, BLACK, (0, 0, 90, 28), 2)

        self.rect = self.image.get_rect()
        self.rect.x = random.choice([55, WIDTH - 145])
        self.rect.y = -60

        self.speed_y = 5
        self.speed_x = random.choice([-2, 2])

    def move(self, road_speed):
        self.rect.y += self.speed_y + road_speed // 4
        self.rect.x += self.speed_x

        if self.rect.left < 35 or self.rect.right > WIDTH - 35:
            self.speed_x *= -1

        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()

        self.kind = random.choice(["nitro", "shield", "repair"])
        self.spawn_time = time.time()
        self.timeout = 6

        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)

        if self.kind == "nitro":
            color = CYAN
            letter = "N"
        elif self.kind == "shield":
            color = BLUE
            letter = "S"
        else:
            color = GREEN
            letter = "R"

        pygame.draw.circle(self.image, color, (20, 20), 19)
        pygame.draw.circle(self.image, BLACK, (20, 20), 19, 2)

        font = pygame.font.SysFont("Verdana", 18, bold=True)
        text = font.render(letter, True, WHITE)
        self.image.blit(text, text.get_rect(center=(20, 20)))

        self.rect = self.image.get_rect()
        self.rect.centerx = safe_lane(player_rect)
        self.rect.y = -random.randint(120, 550)
        self.speed = 4

    def move(self, road_speed):
        self.rect.y += self.speed + road_speed // 3

        if self.rect.top > HEIGHT:
            self.kill()

        if time.time() - self.spawn_time > self.timeout:
            self.kill()


def draw_background(screen, bg_y):
    screen.fill((30, 120, 45))

    road_left = 40
    road_width = WIDTH - 80
    lane_width = road_width // 4

    # road with 4 lanes
    pygame.draw.rect(screen, (190, 190, 190), (road_left, 0, road_width, HEIGHT))

    # yellow road borders
    pygame.draw.rect(screen, YELLOW, (road_left, 0, 4, HEIGHT))
    pygame.draw.rect(screen, YELLOW, (road_left + road_width - 4, 0, 4, HEIGHT))

    # white lane marks
    for line_x in [road_left + lane_width, road_left + lane_width * 2, road_left + lane_width * 3]:
        for y in range(-100, HEIGHT + 100, 150):
            mark_y = (y + bg_y) % (HEIGHT + 150) - 100
            pygame.draw.rect(screen, WHITE, (line_x - 4, mark_y, 8, 70))


def draw_hud(screen, font, score, coins, distance, active_power, power_time, shield):
    remaining = max(0, FINISH_DISTANCE - int(distance))

    texts = [
        f"Score: {int(score)}",
        f"Coins: {coins}",
        f"Distance: {int(distance)}m",
        f"Remaining: {remaining}m",
        f"Power: {active_power if active_power else 'None'}",
        f"Time: {power_time:.1f}s" if active_power == "nitro" else "",
        f"Shield: {'ON' if shield else 'OFF'}"
    ]

    y = 10
    for text in texts:
        if text:
            image = font.render(text, True, BLACK)
            screen.blit(image, (10, y))
            y += 24


def run_game(screen, username, settings):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 18)

    crash_sound = pygame.mixer.Sound(str(ASSET_DIR / "crash.wav"))
    coin_sound = pygame.mixer.Sound(str(ASSET_DIR / "money.wav"))
    power_sound = pygame.mixer.Sound(str(ASSET_DIR / "bip.wav"))

    if settings["sound"]:
        pygame.mixer.music.load(str(ASSET_DIR / "background.wav"))
        pygame.mixer.music.play(-1)

    difficulty_name = settings.get("difficulty", "normal")
    difficulty = DIFFICULTY_DATA[difficulty_name]

    player = Player()

    all_sprites = pygame.sprite.Group()
    traffic_sprites = pygame.sprite.Group()
    coin_sprites = pygame.sprite.Group()
    obstacle_sprites = pygame.sprite.Group()
    power_sprites = pygame.sprite.Group()

    all_sprites.add(player)

    running = True
    won = False

    bg_y = 0
    road_speed = 5
    distance = 0
    score = 0
    coins = 0

    shield = False
    active_power = None
    power_end = 0

    last_traffic_spawn = pygame.time.get_ticks()
    last_coin_spawn = pygame.time.get_ticks()
    last_obstacle_spawn = pygame.time.get_ticks()
    last_power_spawn = pygame.time.get_ticks()
    last_event_spawn = pygame.time.get_ticks()

    while running:
        now = pygame.time.get_ticks()
        level = 1 + int(distance // 600)

        traffic_delay = max(250, difficulty["traffic_delay"] - level * 70)
        obstacle_delay = max(350, difficulty["obstacle_delay"] - level * 70)
        enemy_speed = difficulty["enemy_speed"] + level

        if active_power == "nitro":
            if time.time() > power_end:
                active_power = None
                road_speed = 5 + level
            else:
                road_speed = 10 + level
        else:
            road_speed = 5 + level

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit", {
                    "score": int(score),
                    "distance": int(distance),
                    "coins": coins
                }

        if now - last_traffic_spawn > traffic_delay:
            traffic = TrafficCar(player.rect, enemy_speed)
            traffic_sprites.add(traffic)
            all_sprites.add(traffic)
            last_traffic_spawn = now

        if now - last_coin_spawn > 1050:
            coin = Coin(player.rect)
            coin_sprites.add(coin)
            all_sprites.add(coin)
            last_coin_spawn = now

        if now - last_obstacle_spawn > obstacle_delay:
            obstacle = Obstacle(player.rect)
            obstacle_sprites.add(obstacle)
            all_sprites.add(obstacle)
            last_obstacle_spawn = now

        if now - last_power_spawn > 6500:
            power = PowerUp(player.rect)
            power_sprites.add(power)
            all_sprites.add(power)
            last_power_spawn = now

        if now - last_event_spawn > 5000:
            barrier = MovingBarrier()
            obstacle_sprites.add(barrier)
            all_sprites.add(barrier)
            last_event_spawn = now

        player.move()

        for traffic in list(traffic_sprites):
            traffic.move(road_speed)

        for coin in list(coin_sprites):
            coin.move(road_speed)

        for obstacle in list(obstacle_sprites):
            obstacle.move(road_speed)

        for power in list(power_sprites):
            power.move(road_speed)

        bg_y += road_speed
        if bg_y >= HEIGHT:
            bg_y = 0

        distance += road_speed * 0.08
        score += road_speed * 0.03

        for coin in pygame.sprite.spritecollide(player, coin_sprites, True):
            coins += 1
            score += coin.value

            if settings["sound"]:
                coin_sound.play()

        for power in pygame.sprite.spritecollide(player, power_sprites, True):
            if active_power is None and not shield:
                if settings["sound"]:
                    power_sound.play()

                if power.kind == "nitro":
                    active_power = "nitro"
                    power_end = time.time() + 4

                elif power.kind == "shield":
                    shield = True

                elif power.kind == "repair":
                    score += 50
                    for obstacle in list(obstacle_sprites):
                        obstacle.kill()
                        break

        hit_traffic = pygame.sprite.spritecollideany(player, traffic_sprites)
        hit_obstacle = pygame.sprite.spritecollideany(player, obstacle_sprites)

        if hit_traffic or hit_obstacle:
            if shield:
                shield = False

                if hit_traffic:
                    hit_traffic.kill()

                if hit_obstacle:
                    hit_obstacle.kill()

            else:
                if settings["sound"]:
                    crash_sound.play()
                running = False

        if distance >= FINISH_DISTANCE:
            won = True
            running = False

        draw_background(screen, bg_y)

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        draw_hud(screen,font,score,coins,distance,active_power,max(0, power_end - time.time()),shield)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.mixer.music.stop()

    final_score = int(score + distance * 0.5 + coins * 20)
    add_score(username, final_score, distance, coins)

    return "game_over", {
        "score": final_score,
        "distance": int(distance),
        "coins": coins,
        "won": won
    }
