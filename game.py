import pygame,sys
#pygame setup
pygame.init()

display = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.display.set_caption("Top Down Shooter")

#player class
'''class Player(pygame.sprite.Sprite):
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
        self.human = human'''

#player input dictionary 
player_input = {"left": False, "right": False, "up":False, "down":False}
#other stuff with player 
player_velocity = [0,0] #x and y 
player_speed = 5
playerx = 500
playery= 500 

#function for checking inputs
def check_inputs(key,value):
    if key == pygame.K_a:
        player_input["left"] = value
    elif key == pygame.K_s:
        player_input["down"] = value
    elif key == pygame.K_d:
        player_input["right"] = value
    elif key == pygame.K_w:
        player_input["up"] = value

#game loop
while True:
    display.fill((24,164,86))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_inputs(event.key,True)
        elif event.type == pygame.KEYUP:
            check_inputs(event.key,False)
    #player movement
    player_velocity[0] = player_input["right"] - player_input["left"]
    player_velocity[1] = player_input["down"] - player_input["up"]

    #player
    pygame.draw.circle(display,(255,0,0),(playerx,playery),50)
    playerx += player_velocity[0] * player_speed
    playery += player_velocity[1] * player_speed
    clock.tick(60)
    pygame.display.update()