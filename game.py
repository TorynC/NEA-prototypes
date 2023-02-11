import pygame,sys
#pygame setup
pygame.init()
pygame.font.get_init()

TEXT_FONT = pygame.font.Font("assets/font.otf", 32)

WINDOWSIZE = (1280,720)

DISPLAY = pygame.display.set_mode(WINDOWSIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Top Down Shooter")

HORIZONTAL = 1
UP = 2 
DOWN = 0 

objects = []
bullets = []
enemies = []

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface= pygame.display.get_surface()
        self.ground_surf = pygame.image.load('assets/background.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2

    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self,player):

        self.center_target_camera(player)

        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf,ground_offset)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)


#Class for projectiles and other objects 
class Object:
    def __init__(self,x,y,width,height,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0,0]
        self.collider = [width,height]

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
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.health = self.max_health = 3 #double assignment
        self.image = pygame.transform.scale(pygame.image.load("assets/test.png").convert_alpha(),(64,64))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0,-26)
        self.speed = 5
        self.direction = pygame.math.Vector2()

        self.frame_count = 0 
        self.import_player_assets()
        self.status = 'idle'
        self.animation_speed = 0.15

    def import_player_assets(self):
        #dictionary of animations 
        self.animations = {"up":[pygame.transform.scale(pygame.image.load("assets/player sprite/tile006.png").convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load("assets/player sprite/tile007.png").convert_alpha(),(64,64)),
pygame.transform.scale(pygame.image.load("assets/player sprite/tile008.png").convert_alpha(),(64,64))],
        "down":[pygame.transform.scale(pygame.image.load("assets/player sprite/tile001.png").convert_alpha(),(64,64)),
pygame.transform.scale(pygame.image.load("assets/player sprite/tile002.png").convert_alpha(),(64,64))],
        "right":[pygame.transform.scale(pygame.image.load("assets/player sprite/tile003.png").convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load("assets/player sprite/tile004.png").convert_alpha(),(64,64)),
pygame.transform.scale(pygame.image.load("assets/player sprite/tile005.png").convert_alpha(),(64,64))],
        "left":[pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile003.png").convert_alpha(),True,False),(64,64)),pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile004.png").convert_alpha(),True,False),(64,64)),
pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile005.png").convert_alpha(),True,False),(64,64))],
        "idle":[pygame.transform.scale(pygame.image.load("assets/player sprite/tile000.png").convert_alpha(),(64,64))]}

    def input(self):
        keys = pygame.key.get_pressed()

        #movement input 
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def move(self,speed):
        if self.direction.magnitude()!=0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x *speed
        self.rect.y += self.direction.y * speed 

    def get_status(self):
        #idle_status
        if self.direction.x == 0 and self.direction.y == 0:
            if self.status != 'idle':
                self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]
        #loop over frame counter
        self.frame_count += self.animation_speed
        if self.frame_count >= len(animation):
            self.frame_count = 0
        #set the image
        self.image = animation[int(self.frame_count)]
        self.rect = self.image.get_rect(center =self.hitbox.center )

    def update(self):
        self.input()
        self.move(self.speed)
        self.get_status()
        self.animate()
        

#enemy class
class Enemy(Living):
    def __init__(self,x,y,width,height,tileset,speed):
        super().__init__(x,y,width,height,tileset,speed)
        self.health = 3
        #self.collider = [width/2.5,height/1.5] 
        enemies.append(self)

    def update(self):
        playerx = player.rect.x
        playery = player.rect.y
        enemy_center = self.get_center()

        self.velocity = [playerx-enemy_center[0],playery-enemy_center[1]]
        
        magnitude = (self.velocity[0]**2 + self.velocity[1]**2) ** 0.5
        self.velocity =  [self.velocity[0]/magnitude*self.speed, self.velocity[1]/magnitude*self.speed]

        super().update()

    def change_direction(self):
        super().change_direction()

        if self.velocity[1] > self.velocity[0] > 0:
            self.direction = DOWN
        elif self.velocity[1] < self.velocity[0] <0:
            self.direction = UP
    
    def take_damage(self,damage):
        self.health -= damage
        if self.health <= 0:
            global score
            score += 10
            self.destroy()

    def destroy(self):
        objects.remove(self)
        enemies.remove(self)

score = 0 

is_game_over = False
#player input dictionary 


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
camera_group = CameraGroup()
player = Player((600,400),camera_group)
#target = Object(0,0,50,50,pygame.image.load("assets/cursor.png"))
#enemy = Enemy(200,200,75,75,"assets/enemy-Sheet.png",2)


#pygame.mouse.set_visible(False) #makes mouse cursor invicible 


def display_ui():
    for i in range(player.max_health):
        img = pygame.image.load("assets/heart_empty.png" if i >= player.health else "assets/heart.png")
        img = pygame.transform.scale(img,(50,50))
        DISPLAY.blit(img,(i*50+WINDOWSIZE[0]/2-player.max_health*25,25))

    score_text = TEXT_FONT.render(f'Score: {score}', True, (0,0,0))
    DISPLAY.blit(score_text,(score_text.get_width()/2,25))

def update_screen():
    clock.tick(60)
    pygame.display.update()

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    '''mousePos = pygame.mouse.get_pos() #tuple for position of cursor 
    target.x = mousePos[0] - target.width/2
    target.y = mousePos[1] - target.height/2'''

    #player movement
    '''player.velocity[0] = player_input["right"] - player_input["left"]
    player.velocity[1] = player_input["down"] - player_input["up"]'''

    DISPLAY.fill((24,164,86))
    
    camera_group.update()
    camera_group.custom_draw(player)

    display_ui()

    if is_game_over:
        #pygame.mouse.set_visible(True)
        update_screen()
        continue

    if player.health <= 0:
        if not is_game_over:
            is_game_over = True

    for obj in objects:
        obj.update()

    '''for e in enemies:
        if check_collisions(player,e):
            player.health -= 1
            e.destroy()
            continue
        for b in bullets:
            if check_collisions(b,e):
                e.take_damage(1)
                bullets.remove(b)
                objects.remove(b)'''
    update_screen()
