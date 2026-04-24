import pygame 

class Ball:

    def __init__(self):
        self.x = 400
        self.y = 300
        self.radius = 40
        self.step = 5

    def move(self, keyy, width, height):
        if keyy[pygame.K_UP] and self.y-self.step >= self.radius:
            self.y-=self.step
        if keyy[pygame.K_DOWN] and self.y+self.step <= height - self.radius:
            self.y+=self.step
        if keyy[pygame.K_RIGHT] and self.x+self.step <= width - self.radius:
            self.x+=self.step
        if keyy[pygame.K_LEFT] and self.x-self.step >= self.radius:
            self.x-=self.step
    def draw(self,screen):
        pygame.draw.circle(screen,(255,0,0),(self.x,self.y),self.radius)
