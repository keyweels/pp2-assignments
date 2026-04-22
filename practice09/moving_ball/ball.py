import pygame

class Ball:
    def __init__(self, x, y, radius, speed, width, height):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.width = width
        self.height = height

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.radius - self.speed >= 0:
            self.x -= self.speed

        if keys[pygame.K_RIGHT] and self.x + self.radius + self.speed <= self.width:
            self.x += self.speed

        if keys[pygame.K_UP] and self.y - self.radius - self.speed >= 0:
            self.y -= self.speed

        if keys[pygame.K_DOWN] and self.y + self.radius + self.speed <= self.height:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)