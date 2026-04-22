import pygame
from ball import balls

pygame.init()

width=500
height=500

white_color=(255,255,255)
red_color=(255,0,0)

screen= pygame.display.set_mode((width,height))
clock= pygame.time.Clock()

our_ball=balls(
    x=50,
    y=50,
    radius=25,
    color=red_color,
    screen_width=width,
    screen_height=height
)

running=True

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                our_ball.move_left()
            if event.key==pygame.K_RIGHT:
                our_ball.move_right()
            if event.key==pygame.K_DOWN:
                our_ball.move_down()
            if event.key==pygame.K_UP:
                our_ball.move_up()
    screen.fill(white_color)
    our_ball.draw_circle(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()