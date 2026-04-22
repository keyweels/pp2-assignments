import random
import pygame

pygame.init()

WIDTH = 520
HEIGHT = 780
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Racer")
clock = pygame.time.Clock()

BG_TOP = (18, 20, 28)
BG_BOTTOM = (28, 32, 44)
ROAD = (42, 42, 50)
ROAD_EDGE = (210, 210, 220)
LANE = (235, 235, 235)
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (170, 175, 185)
GREEN = (50, 140, 90)
BLUE = (70, 130, 255)
RED = (230, 70, 70)
YELLOW = (255, 210, 70)
PURPLE = (170, 100, 255)

title_font = pygame.font.SysFont("Arial", 44, bold=True)
big_font = pygame.font.SysFont("Arial", 32, bold=True)
font = pygame.font.SysFont("Arial", 24, bold=True)
small_font = pygame.font.SysFont("Arial", 20)

ROAD_X = 80
ROAD_WIDTH = WIDTH - 160
LANES = 3
LANE_WIDTH = ROAD_WIDTH // LANES

road_offset = 0


def draw_gradient():
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))


def lane_center(lane):
    return ROAD_X + lane * LANE_WIDTH + LANE_WIDTH // 2


def lane_x(lane, width):
    return lane_center(lane) - width // 2


class Car:
    def __init__(self, lane, y, color, is_player=False):
        self.width = 56
        self.height = 108
        self.lane = lane
        self.x = lane_x(lane, self.width)
        self.y = y
        self.color = color
        self.is_player = is_player

    def update_lane(self):
        self.x = lane_x(self.lane, self.width)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        shadow = pygame.Surface((self.width + 16, self.height + 16), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 70), (0, self.height - 4, self.width + 16, 20))
        screen.blit(shadow, (self.x - 8, self.y - 2))

        body = pygame.Rect(self.x, self.y, self.width, self.height)
        cabin = pygame.Rect(self.x + 8, self.y + 14, self.width - 16, 30)
        glass = pygame.Rect(self.x + 12, self.y + 18, self.width - 24, 16)

        pygame.draw.rect(screen, self.color, body, border_radius=14)
        pygame.draw.rect(screen, (30, 34, 44), cabin, border_radius=10)
        pygame.draw.rect(screen, (170, 215, 255), glass, border_radius=8)

        pygame.draw.rect(screen, BLACK, (self.x - 4, self.y + 16, 7, 22), border_radius=4)
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 3, self.y + 16, 7, 22), border_radius=4)
        pygame.draw.rect(screen, BLACK, (self.x - 4, self.y + self.height - 38, 7, 22), border_radius=4)
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 3, self.y + self.height - 38, 7, 22), border_radius=4)

        if self.is_player:
            pygame.draw.rect(screen, YELLOW, (self.x + 7, self.y + 5, 12, 5), border_radius=3)
            pygame.draw.rect(screen, YELLOW, (self.x + self.width - 19, self.y + 5, 12, 5), border_radius=3)
            pygame.draw.rect(screen, RED, (self.x + 7, self.y + self.height - 10, 12, 5), border_radius=3)
            pygame.draw.rect(screen, RED, (self.x + self.width - 19, self.y + self.height - 10, 12, 5), border_radius=3)
        else:
            pygame.draw.rect(screen, WHITE, (self.x + 7, self.y + 5, 12, 5), border_radius=3)
            pygame.draw.rect(screen, WHITE, (self.x + self.width - 19, self.y + 5, 12, 5), border_radius=3)
            pygame.draw.rect(screen, RED, (self.x + 7, self.y + self.height - 10, 12, 5), border_radius=3)
            pygame.draw.rect(screen, RED, (self.x + self.width - 19, self.y + self.height - 10, 12, 5), border_radius=3)


class Coin:
    def __init__(self):
        self.radius = 12
        self.reset()

    def reset(self):
        self.lane = random.randint(0, LANES - 1)
        self.x = lane_center(self.lane)
        self.y = random.randint(-600, -120)
        self.value = random.choice([1, 1, 2])

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (255, 235, 160), (self.x - 2, self.y - 2), self.radius - 4)
        pygame.draw.circle(screen, (130, 100, 25), (self.x, self.y), self.radius, 2)

        value_text = small_font.render(str(self.value), True, BLACK)
        value_rect = value_text.get_rect(center=(self.x, self.y))
        screen.blit(value_text, value_rect)


def draw_road():
    pygame.draw.rect(screen, ROAD, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))
    pygame.draw.line(screen, ROAD_EDGE, (ROAD_X, 0), (ROAD_X, HEIGHT), 5)
    pygame.draw.line(screen, ROAD_EDGE, (ROAD_X + ROAD_WIDTH, 0), (ROAD_X + ROAD_WIDTH, HEIGHT), 5)

    for lane in range(1, LANES):
        x = ROAD_X + lane * LANE_WIDTH
        for y in range(-80, HEIGHT + 80, 80):
            pygame.draw.rect(screen, LANE, (x - 3, y + road_offset, 6, 38), border_radius=4)


def draw_hud(coins, distance, level, speed):
    panel = pygame.Surface((WIDTH - 30, 78), pygame.SRCALPHA)
    pygame.draw.rect(panel, (255, 255, 255, 24), (0, 0, WIDTH - 30, 78), border_radius=18)
    screen.blit(panel, (15, 15))

    screen.blit(font.render(f"Coins: {coins}", True, WHITE), (30, 28))
    screen.blit(font.render(f"Dist: {distance}", True, WHITE), (150, 28))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (285, 28))
    screen.blit(font.render(f"Speed: {speed}", True, WHITE), (405, 28))


def draw_countdown(text):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 70))
    screen.blit(overlay, (0, 0))
    countdown_text = title_font.render(text, True, WHITE)
    screen.blit(countdown_text, countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))


def draw_game_over(coins, distance):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    card = pygame.Surface((360, 220), pygame.SRCALPHA)
    pygame.draw.rect(card, (25, 28, 38, 240), (0, 0, 360, 220), border_radius=22)
    screen.blit(card, (80, 260))

    screen.blit(title_font.render("GAME OVER", True, RED), (120, 290))
    screen.blit(big_font.render(f"Coins: {coins}", True, WHITE), (160, 360))
    screen.blit(big_font.render(f"Distance: {distance}", True, WHITE), (135, 400))
    screen.blit(small_font.render("Press R to restart", True, YELLOW), (185, 450))


def reset_game():
    global player, enemies, coins_list, coins_collected, distance, level, game_over
    global enemy_speed, road_speed, road_offset, countdown_active, countdown_value, countdown_timer

    player = Car(1, HEIGHT - 150, BLUE, True)

    enemies = [
        Car(random.randint(0, LANES - 1), -150, RED),
        Car(random.randint(0, LANES - 1), -420, PURPLE),
    ]

    coins_list = [Coin()]
    coins_collected = 0
    distance = 0
    level = 1
    game_over = False

    enemy_speed = 4
    road_speed = 5
    road_offset = 0

    countdown_active = True
    countdown_value = 3
    countdown_timer = pygame.time.get_ticks()


reset_game()
running = True

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over and not countdown_active:
                if event.key == pygame.K_LEFT and player.lane > 0:
                    player.lane -= 1
                    player.update_lane()
                elif event.key == pygame.K_RIGHT and player.lane < LANES - 1:
                    player.lane += 1
                    player.update_lane()

            if game_over and event.key == pygame.K_r:
                reset_game()

    draw_gradient()
    draw_road()

    if countdown_active:
        now = pygame.time.get_ticks()
        if now - countdown_timer >= 1000:
            countdown_value -= 1
            countdown_timer = now
            if countdown_value < 0:
                countdown_active = False

        countdown_text = "GO" if countdown_value == 0 else str(countdown_value)

        for enemy in enemies:
            enemy.draw()
        for coin in coins_list:
            coin.draw()
        player.draw()
        draw_hud(coins_collected, distance, level, enemy_speed)
        draw_countdown(countdown_text)

    elif not game_over:
        distance += 1

        level = 1 + distance // 400
        enemy_speed = min(4 + level - 1, 10)
        road_speed = enemy_speed + 1

        road_offset += road_speed
        if road_offset >= 80:
            road_offset = 0

        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemy.lane = random.randint(0, LANES - 1)
                enemy.update_lane()
                enemy.y = random.randint(-700, -150)

        for coin in coins_list:
            coin.y += road_speed
            if coin.y > HEIGHT:
                coin.reset()

        if len(coins_list) < min(1 + level // 2, 3):
            coins_list.append(Coin())

        player_rect = player.rect()

        for enemy in enemies:
            if player_rect.colliderect(enemy.rect()):
                game_over = True

        for coin in coins_list:
            if player_rect.colliderect(coin.rect()):
                coins_collected += coin.value
                coin.reset()

        for coin in coins_list:
            coin.draw()
        for enemy in enemies:
            enemy.draw()
        player.draw()
        draw_hud(coins_collected, distance, level, enemy_speed)

    else:
        for coin in coins_list:
            coin.draw()
        for enemy in enemies:
            enemy.draw()
        player.draw()
        draw_hud(coins_collected, distance, level, enemy_speed)
        draw_game_over(coins_collected, distance)

    pygame.display.flip()

pygame.quit()