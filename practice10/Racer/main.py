import pygame
import random
import sys


pygame.init()

width=600
height=800
fps=60



screen=pygame.display.set_mode((width,height))
clock=pygame.time.Clock()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
RED = (220, 20, 60)


ROAD_LEFT = 80
ROAD_WIDTH = 440
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 42)
running=True


class player:
    def __init__(self):
        self.width=50
        self.height=90
        self.x=width//2-self.width//2
        self.y=height-120
        self.speed=6

        self.image=pygame.image.load("C:/Users/User/Desktop/Practice Python/PracticePP2/Pygame2/imagess/images.png")
        self.image=pygame.transform.scale(self.image,(self.width,self.height))

        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    def move(self,keys):
        if keys[pygame.K_LEFT]:
            self.x-=self.speed
        if keys[pygame.K_RIGHT]:
            self.x+=self.speed

        if self.x<50:
            self.x=50
        if self.x>400-self.width:
            self.x=400-self.width
        
        self.rect.x=self.x
        self.rect.y=self.y
    
    def draws(self,surface):
        surface.blit(self.image,(self.x,self.y))
    
class enemy:
    def __init__(self):
        self.width=50
        self.height=90
        self.x=random.randint(50,400-self.width)

        self.y=-120
        self.speed=6

        self.image=pygame.image.load("C:/Users/User/Desktop/Practice Python/PracticePP2/Pygame2/imagess/Pygame_rects.webp")
        self.image=pygame.transform.scale(self.image,(self.width,self.height))

        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    def move(self):
        self.y+=self.speed

        if self.y>height:
            self.reset()
        
        self.rect.x=self.x
        self.rect.y=self.y
    def reset(self):
        self.x=random.randint(50,400-self.width)
        self.y=-120
    def update_speed(self, coins_collected):
        self.speed = self.base_speed + (coins_collected // 5)
    def draws(self,surface):
        surface.blit(self.image,(self.x,self.y))

class coin:
    def __init__(self):
        self.size=30
        self.speed = 4

        self.respawn()
    def respawn(self):
        # Random position on the road
        self.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.size)
        self.y = random.randint(-250, -80)

        # Random coin weight
        self.value = random.choice([1, 2, 3])

        # Choose color by weight
        if self.value == 1:
            self.color = GRAY
        elif self.value == 2:
            self.color = RED
        else:
            self.color = BLACK

        # Rectangle used for collision
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self):
        # Move coin down
        self.y += self.speed

        # Respawn coin if it leaves screen
        if self.y > height:
            self.respawn()

        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface):
     
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        pygame.draw.circle(surface, self.color, (center_x, center_y), self.size // 2)
        pygame.draw.circle(surface, BLACK, (center_x, center_y), self.size // 2, 2)



player1=player()
enemy1=enemy()
coins=coin()

coins_colleccted=0
liney=0
line_speed=7
game_over=False

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    if not game_over:
        keys=pygame.key.get_pressed()
        player1.move(keys)
        enemy1.move()
        coins.move()

        liney += line_speed
        if liney >= 40:
            liney = 0

        if player1.rect.colliderect(enemy1.rect):
            game_over = True

   
        if player1.rect.colliderect(coins.rect):
            coins_colleccted += coins.value
            coins.respawn()

        screen.fill(GRAY)

      
        pygame.draw.rect(screen, BLACK, (50, 0, 500, height))

    
        pygame.draw.line(screen, WHITE, (50, 0), (50, height), 5)
        for i in range(-40,height,80):
            pygame.draw.rect(screen, WHITE, (350,i+liney, 10,40))

        for i in range(-40, height, 80):
            pygame.draw.rect(screen, WHITE, (195, i + liney, 10, 40))

  
        player1.draws(screen)
        enemy1.draws(screen)
        coins.draw(screen)


        coin_text = font.render(f"Coins: {coins_colleccted}", True, WHITE)
        value_text = font.render(f"Coin value: {coins.value}", True, WHITE)
        screen.blit(coin_text, (240, 20))
        screen.blit(value_text, (ROAD_RIGHT - 170, 55))

    else:
        screen.fill(WHITE)

        game_over_text = big_font.render("GAME OVER", True, RED)
        result_text = font.render(f"Coins collected: {coins_colleccted}", True, BLACK)
        exit_text = font.render("Close the window to exit", True, BLACK)

        screen.blit(game_over_text, (80, 220))
        screen.blit(result_text, (95, 290))
        screen.blit(exit_text, (80, 340))

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()





        



