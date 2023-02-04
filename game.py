import pygame,sys
#pygame setup
pygame.init()

display = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.display.set_caption("Top Down Shooter")

#Abstract class for player and enemy 
class Entities:
    def __init__(self,x,y,width,height,image):
        self.x=x
        self.y = y
        self.width = width
        self.image = image
        self.velocity = [0,0]

    def draw(self):
        display.blit(pygame.transform.scale(self.image,(self.width,self.height)),(self.x,self.y))
    
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

#player class
class Player(Entities):
    def __init__(self,image,x,y,width,height):
        super().__init__()

#enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,human):
        super().__init__()
        self.human = human

#player input dictionary 
player_input = {"left": False, "right": False, "up":False, "down":False}
#other stuff with player 
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

#objects
test_object = 

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