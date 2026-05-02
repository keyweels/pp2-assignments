import pygame
import random
import time

pygame.init()

WIDTH = 400
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

clock = pygame.time.Clock()

image_background = pygame.image.load("resources/AnimatedStreet.png")
image_player = pygame.image.load("resources/Player.png")
image_enemy = pygame.image.load("resources/Enemy.png")

coin_images = {
    20: pygame.image.load("resources/20tg.png"),
    50: pygame.image.load("resources/50tg.png"),
    100: pygame.image.load("resources/100tg.png")
}

pygame.mixer.music.load("resources/background.wav")
pygame.mixer.music.play(-1)

sound_crash = pygame.mixer.Sound("resources/crash.wav")
sound_get_tenge = pygame.mixer.Sound("resources/money.wav")
sound_bip = pygame.mixer.Sound("resources/bip.wav")

font_game_over = pygame.font.SysFont("Verdana", 60)
image_game_over = font_game_over.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

font_score = pygame.font.SysFont("Verdana", 18)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)

        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 7
        self.generate_random_rect()

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.generate_random_rect()


class Money(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.generate_random_coin()

        self.rect = self.image.get_rect()
        self.generate_random_rect()

    def generate_random_coin(self):
        self.value = random.choice([20, 50, 100])
        self.image = coin_images[self.value]

        if self.value == 20:
            self.image = pygame.transform.scale(self.image, (30, 30))

        elif self.value == 50:
            self.image = pygame.transform.scale(self.image, (40, 40))

        elif self.value == 100:
            self.image = pygame.transform.scale(self.image, (50, 50))

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = random.randint(100, HEIGHT - self.rect.height)

    def respawn(self):
        self.generate_random_coin()
        self.rect = self.image.get_rect()
        self.generate_random_rect()


player = Player()
enemy = Enemy()
tenge = Money()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
tenge_sprites = pygame.sprite.Group()

all_sprites.add(player, enemy)
enemy_sprites.add(enemy)
tenge_sprites.add(tenge)

score = 0
next_speed_score = 300

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sound_bip.play()

    screen.blit(image_background, (0, 0))
    screen.blit(tenge.image, tenge.rect)
    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)

    image_score = font_score.render(f"Score: {score} tg", True, "black")
    image_score_rect = image_score.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(image_score, image_score_rect)

    if pygame.sprite.spritecollideany(player, tenge_sprites):
        sound_get_tenge.play()
        score += tenge.value

        print(f"You collected {tenge.value} tg")

        if score >= next_speed_score:
            enemy.speed += 1
            next_speed_score += 300
            print("Enemy speed increased!")

        tenge.respawn()

    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()

        time.sleep(2)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()