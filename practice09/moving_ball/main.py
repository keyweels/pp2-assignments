import pygame
from ball import Ball
pygame.init()
ball = Ball()

width = 800
height = 600

white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

x = width // 2
y = height // 2

step = 5
radius = 40

running = True

screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            
    keyy = pygame.key.get_pressed()
    ball.move(keyy,width,height)
        
    screen.fill(white)
    
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()