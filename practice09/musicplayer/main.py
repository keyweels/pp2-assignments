import pygame
from musicplayer import player


pygame.init()

pygame.mixer.init()

screen=pygame.display.set_mode((800,600))

white_color=(255,255,255)

font= pygame.font.SysFont("Arial",28)
small_font=pygame.font.SysFont("Arial",22)

playlist=["C:/Users/User/Desktop/Practice Python/PracticePP2/Sound(music)/PianoDeuss_-_Never_meant_to_belong_(SkySound.cc).mp3",
          "C:/Users/User/Desktop/Practice Python/PracticePP2/Sound(music)/Stein_gate_OST_-_Christina_(SkySound.cc).mp3"]

avplayer=player(playlist)


clock=pygame.time.Clock()


running=True


while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_p:
                avplayer.play()
            if event.key==pygame.K_s:
                avplayer.stop()
            if event.key==pygame.K_b:
                avplayer.previous_track()
            if event.key==pygame.K_n:
                avplayer.next_track()
            if event.key==pygame.K_q:
                running=False
    screen.fill(white_color)
    title_text = font.render("Music Player", True, (255,0,0))
    track_text = small_font.render(f"Track: {avplayer.status()}", True, (255,0,0))
    controls_text = small_font.render("P=Play  S=Stop  N=Next  B=Back  Q=Quit", True,(255,0,0))
    screen.blit(title_text, (250, 40))
    screen.blit(track_text, (180, 110))
    screen.blit(controls_text, (90, 220))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

    