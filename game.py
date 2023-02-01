import pygame,sys

#pygame setup
pygame.init()

display = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.display.set_caption("Top Down Shooter")

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('tile000.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
    
    
#enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,human):
        super().__init__()
        self.human = human

#player input dictionary 
player_input = {"left": False, "right": False, "up":False, "down":False}


#game loop
while True:
    display.fill((24,164,86))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_input["left"] = True


    pygame.draw.rect(display,(255,0,0),(100,100,32,32))

    clock.tick(60)
    pygame.display.update()