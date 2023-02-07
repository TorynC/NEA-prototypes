import pygame,sys
#pygame setup
pygame.init()
WINDOWSIZE = (1280,720)

DISPLAY = pygame.display.set_mode(WINDOWSIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Top Down Shooter")

HORIZONTAL = 1
UP = 2 
DOWN = 0 

objects = []

#Class for projectiles and other objects 
class Object:
    def __init__ (self,x,y,width,height,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0,0]

        objects.append(self)
    def draw(self):
        DISPLAY.blit(pygame.transform.scale(self.image,(self.width,self.height)),(self.x,self.y))

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def get_center(self):
        return self.x + self.width/2, self.y + self.height/2

#Abstract class for player and enemy 
class Living(Object):
    def __init__(self,x,y,width,height,tileset,speed):
        super().__init__(x,y,width,height,None)

        self.speed = speed
        self.tileset = load_tileset(tileset,16,16)
        self.direction = 0
        self.flipx = False
        self.frame = 0
        self.frames = [0,1,0,2]
        self.frame_timer = 0

    def change_direction(self):
        if self.velocity[0] < 0:
            self.direction = HORIZONTAL
            self.flipx = True
        elif self.velocity[0] > 0:
            self.direction = HORIZONTAL
            self.flipx = False
        elif self.velocity[1] >0:
            self.direction = DOWN
        elif self.velocity[1]<0:
            self.direction = UP

    def draw(self):
        image = pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction], (self.width,self.height))
        self.change_direction()
        image = pygame.transform.flip(image,self.flipx,False)
        DISPLAY.blit(image,(self.x,self.y))
        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.frame = 0
            return
        self.frame_timer += 1
        if self.frame_timer <10:
            return
        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0
        self.frame_timer = 0

    def update(self):
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()

#player class
class Player(Living):
    def __init__(self,x,y,width,height,tileset,speed):
        super().__init__(x,y,width,height,tileset,speed)


#enemy class
'''class Enemy(Living):
    def __init__(self,x,y,human):
        super().__init__()
        self.human = human'''

#player input dictionary 
player_input = {"left": False, "right": False, "up":False, "down":False}

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

def load_tileset(file,width,height):
    image = pygame.image.load(file).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    for tile_x in range(0,image_width//width):
        line = []
        tileset.append(line)
        for tile_y in range(0,image_height//height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tileset

#objects
player = Player(WINDOWSIZE[0]/2,WINDOWSIZE[1]/2,75,75,"assets/player-Sheet.png",5)
target = Object(0,0,50,50,pygame.image.load("assets/cursor.png"))

pygame.mouse.set_visible(False) #makes mouse cursor invicible 

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_inputs(event.key,True)
        elif event.type == pygame.KEYUP:
            check_inputs(event.key,False)
    
    mousePos = pygame.mouse.get_pos() #tuple for position of cursor 
    target.x = mousePos[0] - target.width/2
    target.y = mousePos[1] - target.height/2

    #player movement
    player.velocity[0] = player_input["right"] - player_input["left"]
    player.velocity[1] = player_input["down"] - player_input["up"]

    DISPLAY.fill((24,164,86))
    for obj in objects:
        obj.update()

    clock.tick(60)
    pygame.display.update()