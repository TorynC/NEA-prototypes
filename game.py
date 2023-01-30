import pygame,sys

#pygame setup
pygame.init()

display = pygame.display.set_mode((1000,1000))
clock = pygame.time.Clock()
pygame.display.set_caption("Top Down Shooter")

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface([50,45])
        self.image.fill((10,10,120))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.change_x = 0
        self.change_y = 0

#enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,human):
        super().__init__()
        self.human = human
        self.image = pygame.Surface([50,45])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0

spritelist = pygame.sprite.Group()
player = Player(50,50)
spritelist.add(player)
enemy1 = Enemy(500,50,player)
spritelist.add(enemy1)

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    spritelist.update()
    spritelist.draw(display)

    clock.tick(60)
    pygame.display.update()
    



