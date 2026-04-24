import pygame
from player import Music

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

music = Music()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                music.play()

            if event.key == pygame.K_s:
                music.stop()

            if event.key == pygame.K_n:
                music.next()

            if event.key == pygame.K_b:
                music.back()

            if event.key == pygame.K_q:
                running = False

    screen.fill(WHITE)

    title_text = font.render("Music Player", True, BLACK)
    screen.blit(title_text, (300, 80))

    controls_text = font.render("P - Play | S - Stop | N - Next | B - Back | Q - Quit", True, BLACK)
    screen.blit(controls_text, (70, 180))

    current_track_text = font.render(f"Current track: {music.get_current_track_name()}", True, BLACK)
    screen.blit(current_track_text, (180, 280))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()