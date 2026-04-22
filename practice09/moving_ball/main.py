import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

ball = Ball(
    x=WIDTH // 2,
    y=HEIGHT // 2,
    radius=25,
    speed=20,
    width=WIDTH,
    height=HEIGHT
)

running = True

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    ball.move(keys)

    ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()