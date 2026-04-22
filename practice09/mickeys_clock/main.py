import os
import pygame
from clock import MickeyClock

pygame.init()

WIDTH = 800
HEIGHT = 800
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

fps_clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, "images")

background = pygame.image.load(os.path.join(IMAGES_DIR, "clock.png")).convert_alpha()
right_hand = pygame.image.load(os.path.join(IMAGES_DIR, "rightarm.png")).convert_alpha()
left_hand = pygame.image.load(os.path.join(IMAGES_DIR, "leftarm.png")).convert_alpha()

mickey_clock = MickeyClock(
    screen=screen,
    center=(WIDTH // 2, HEIGHT // 2),
    background=background,
    right_hand=right_hand,
    left_hand=left_hand
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    mickey_clock.draw()

    pygame.display.flip()
    fps_clock.tick(60)

pygame.quit()