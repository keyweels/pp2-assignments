import pygame
from clock import MickeyClock

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

clock = pygame.time.Clock()

mickey_clock = MickeyClock(
    screen=screen,
    center=(WIDTH // 2, HEIGHT // 2),
    background_path="C:/Users/User/Desktop/Practice Python/PracticePP2/Pygame/mickey_clock_true/images/clock.png",
    minute_hand_path="C:/Users/User/Desktop/Practice Python/PracticePP2/Pygame/mickey_clock_true/images/hour_hand.png",
    second_hand_path="C:/Users/User/Desktop/Practice Python/PracticePP2/Pygame/mickey_clock_true/images/second_hand.png"
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    mickey_clock.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()