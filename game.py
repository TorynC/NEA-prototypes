import pygame,sys

#pygame setup
pygame.init()
screen = pygame.display.set_mode((1300,750))
clock = pygame.time.Clock()

while True:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(60)
    pygame.display.update()

    worldmap = [0,1,2,3,4,45,5,65,6,7,78]


