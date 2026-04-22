import pygame
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font_big = pygame.font.SysFont("Arial", 40)
font = pygame.font.SysFont("Arial", 24)

BASE_DIR = os.path.join(os.path.dirname(__file__), "music")

# === ТВОИ ТРЕКИ ===
playlist = [
    os.path.join(BASE_DIR, "angga-renggana-t_lukas-graham-7-years.mp3"),
    os.path.join(BASE_DIR, "eminem-mockingbird.mp3"),
    os.path.join(BASE_DIR, "Stan (mp3store.live).mp3"),
]

# === КРАСИВЫЕ НАЗВАНИЯ ===
track_names = [
    "Seven Years",
    "Mockingbird",
    "Stan"
]

index = 0
playing = False
start_ticks = 0


def play():
    global playing, start_ticks
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()
    start_ticks = pygame.time.get_ticks()
    playing = True


def stop():
    global playing
    pygame.mixer.music.stop()
    playing = False


def next_track():
    global index
    index = (index + 1) % len(playlist)
    play()


def prev_track():
    global index
    index = (index - 1) % len(playlist)
    play()


running = True
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play()
            elif event.key == pygame.K_s:
                stop()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                prev_track()
            elif event.key == pygame.K_q:
                running = False

    # === UI ===
    title = font_big.render("Music Player", True, (0, 0, 0))
    screen.blit(title, (WIDTH // 2 - 130, 50))

    track_text = font.render(f"Current track: {track_names[index]}", True, (0, 0, 0))
    screen.blit(track_text, (WIDTH // 2 - 200, 150))

    if playing:
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    else:
        seconds = 0

    time_text = font.render(f"Position: {seconds} sec", True, (0, 0, 0))
    screen.blit(time_text, (WIDTH // 2 - 100, 200))

    tracks_count = font.render(f"Tracks found: {len(playlist)}", True, (0, 0, 0))
    screen.blit(tracks_count, (WIDTH // 2 - 100, 250))

    controls = font.render("P - Play | S - Stop | N - Next | B - Previous | Q - Quit", True, (0, 100, 200))
    screen.blit(controls, (WIDTH // 2 - 300, 320))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()