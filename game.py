import pygame
import sys
import math
import random
import sqlite3

game_active = False

class SQL: #database class 
    def __init__(self,database):
        self.database = database
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor() 
        self.score = 0
        self.time = 0
        self.id = self.cursor.execute("SELECT AttemptID FROM LoggedIn").fetchall()
        self.all_id = []
 
    def add_to_database(self):  #method to update data in database for when user plays the game 
        update_query = "UPDATE LoggedIn SET Score = ? , Time = ? WHERE AttemptID = ?"
        data = (self.score,self.time,self.id)
        self.cursor.execute(update_query,data) 
        self.connection.commit()
        
    def get_last_id(self): #method to obtain the newest attempt ID in LoggedIn table in database to update the score and time associated with that ID
        for id in self.id:
            self.all_id.append(int(id[0]))
        self.all_id.sort()
        self.id = self.all_id[-1]

class Player(pygame.sprite.Sprite): #player class inherits from sprite class from pygame
    def __init__(self):
        super().__init__() #super constructor to inherit from sprite class 
        self.health = self.max_health = 3 #double assignment 
        self.image = pygame.transform.scale(pygame.image.load(
            "assets/player sprite/tile000.png").convert_alpha(), (40, 40))
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.speed = 5
        self.direction = pygame.math.Vector2()
        self.bullets = pygame.sprite.Group()

        self.frame_count = 0
        self.import_player_assets()
        self.status = 'idle'
        self.animation_speed = 0.15

    def import_player_assets(self):
        #method to get animations of player that match with movement input from user 
        #animations stored in a dictionary 
        self.animations = {"up": [pygame.transform.scale(pygame.image.load("assets/player sprite/tile006.png").convert_alpha(), (40, 40)), pygame.transform.scale(pygame.image.load("assets/player sprite/tile007.png").convert_alpha(), (40, 40)),
                                  pygame.transform.scale(pygame.image.load("assets/player sprite/tile008.png").convert_alpha(), (40, 40))],
                           "down": [pygame.transform.scale(pygame.image.load("assets/player sprite/tile001.png").convert_alpha(), (40, 40)),
                                    pygame.transform.scale(pygame.image.load("assets/player sprite/tile002.png").convert_alpha(), (40, 40))],
                           "right": [pygame.transform.scale(pygame.image.load("assets/player sprite/tile003.png").convert_alpha(), (40, 40)), pygame.transform.scale(pygame.image.load("assets/player sprite/tile004.png").convert_alpha(), (40, 40)),
                                     pygame.transform.scale(pygame.image.load("assets/player sprite/tile005.png").convert_alpha(), (40, 40))],
                           "left": [pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile003.png").convert_alpha(), True, False), (40, 40)), pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile004.png").convert_alpha(), True, False), (40, 40)),
                                    pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile005.png").convert_alpha(), True, False), (40, 40))],
                           "idle": [pygame.transform.scale(pygame.image.load("assets/player sprite/tile000.png").convert_alpha(), (40, 40))]}

    def input(self): #method to check user inputs and change player sprite status to change animation 
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = "down"
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

        if keys[pygame.MOUSEBUTTONDOWN]:
            self.shoot()

    def move(self, speed): #method to move player sprite based on user inputs 
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #normalize movement vector so when player sprite moves diagonally the speed is consistent 

        self.rect.centerx += self.direction.x * speed
        self.rect.centery += self.direction.y * speed

        #collision check with map border by checking position of player sprite rectangle with position of map borders 
        if self.rect.right >= 1220:
            self.rect.right = 1220 
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.bottom >= 670:
            self.rect.bottom = 670
        if self.rect.top <= 20:
            self.rect.top = 20

    def reset_status(self):
        #if player is not moving the status is set to idle 
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'

    def animate(self):
        #animate player sprite based on movement, uses dictionary from above 
        animation = self.animations[self.status]

        self.frame_count += self.animation_speed
        if self.frame_count >= len(animation):
            self.frame_count = 0

        self.image = animation[int(self.frame_count)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self): 
        #shoot bullets at cursor from player position 
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(
            (self.rect.centery-mouse_pos[1]), (self.rect.centerx-mouse_pos[0]))
        #angle from player to cursor is calculated using tangent of the differences in vectors between player and cursor  
        self.bullets.add(Bullet(angle, self.rect.centerx, self.rect.centery))
        #bullet sprite group 
        #bullet object instantiated inside player class (composition) and added to bullet sprite group 
    
    def bullet_delete(self):
        for bullet in self.bullets:
            if bullet.rect.centerx >= SCREEN_WIDTH or bullet.rect.centerx <= 0:
                bullet.kill()
            elif bullet.rect.centery >= SCREEN_HEIGHT or bullet.rect.centery <= 0:
                bullet.kill()

    def update(self):
        #calls important methods 
        self.input()
        self.reset_status()
        self.animate()
        self.move(self.speed)
        DISPLAY.blit(self.image,(self.rect.centerx,self.rect.centery))

class Enemy(pygame.sprite.Sprite):
    #enemy class inherits from sprite class 
    def __init__(self, x, y,speed):
        super().__init__() 
        self.x = x
        self.y = y
        self.speed = speed

    def update(self): #method used to animate the enemy sprites and create enemy AI to follow player 

        if self.animationcount + 1 == 12:
            self.animationcount = 0
        self.animationcount += 1

        if game.player.rect.centerx > self.rect.centerx:
            self.rect.centerx += self.speed
        elif game.player.rect.centerx < self.rect.centerx:
            self.rect.centerx -= self.speed

        if game.player.rect.centery > self.rect.centery :
            self.rect.centery += self.speed
        elif game.player.rect.centery < self.rect.centery :
            self.rect.centery -= self.speed

        DISPLAY.blit(self.animations[self.animationcount//4], (self.rect.centerx
                     , self.rect.centery))

class Slime(Enemy): #slime class inherits enemy class and sprite class (multiple inheritence)
    def __init__(self,x,y,speed):
        super().__init__(x,y,speed)
        self.animationcount = 0
        self.image = pygame.transform.scale(pygame.image.load(
            "assets/enemy sprite 3/slime_animation_0.png").convert_alpha(), (40, 40))
        self.animations = [pygame.transform.scale(pygame.image.load("assets/enemy sprite 3/slime_animation_0.png").convert_alpha(), (40, 40)),
                           pygame.transform.scale(pygame.image.load(
                               "assets/enemy sprite 3/slime_animation_1.png").convert_alpha(), (40, 40)),
                           pygame.transform.scale(pygame.image.load("assets/enemy sprite 3/slime_animation_2.png").convert_alpha(), (40, 40))]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.health = 1

class Skeleton1(Enemy): #skeleton1 class inherits from enemy class and sprite class
    def __init__(self,x,y,speed):
        super().__init__(x,y,speed)
        self.animationcount = 0
        self.image = pygame.transform.scale(pygame.image.load("assets/enemy sprite 1/tile000.png").convert_alpha(),(40,40))
        self.animations = [pygame.transform.scale(pygame.image.load("assets/enemy sprite 1/tile000.png").convert_alpha(), (40, 40)),
                           pygame.transform.scale(pygame.image.load(
                               "assets/enemy sprite 1/tile001.png").convert_alpha(), (40, 40)),
                           pygame.transform.scale(pygame.image.load("assets/enemy sprite 1/tile002.png").convert_alpha(), (40, 40))]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.health = 2

class Skeleton2(Enemy): #skeleton2 class inherits from enemy class and sprite class
    def __init__(self,x,y,speed):
        super().__init__(x,y,speed)
        self.animationcount = 0
        self.image = pygame.transform.scale(pygame.image.load("assets/enemy sprite 2/E2-tile000.png").convert_alpha(),(40,40))
        self.animations = [pygame.transform.scale(pygame.image.load("assets/enemy sprite 2/E2-tile000.png").convert_alpha(), (40, 40)),
                           pygame.transform.scale(pygame.image.load(
                               "assets/enemy sprite 2/E2-tile001.png").convert_alpha(), (40, 40)),
                           pygame.transform.scale(pygame.image.load("assets/enemy sprite 2/E2-tile002.png").convert_alpha(), (40, 40))]
        self.health = 3
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.lasers = pygame.sprite.Group()
        self.ready = True
        self.cooldown = 1000
        self.attack_time = 0
    
    def update(self): #overriding of update method from parent class
        if self.animationcount + 1 == 12:
            self.animationcount = 0
        self.animationcount += 1
        
        DISPLAY.blit(self.animations[self.animationcount//4], (self.rect.centerx
                     , self.rect.centery))
        self.attack()
        self.recharge()
        self.laser_collision()
        self.laser_delete()
        for laser in self.lasers:
                laser.move()
                self.lasers.draw(DISPLAY) 
        
    def recharge(self): #method to recharge enemy laser 
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time -self.attack_time >= self.cooldown:
                self.ready = True

    def attack(self): #method to shoot enemy laser vertically downwards 
        if self.ready:
            self.lasers.add(Enemy_laser(self.rect.centerx,self.rect.centery)) #enemy laser object is composed inside skeleton2 class and added to lasers sprite group 
            self.ready = False
            self.attack_time = pygame.time.get_ticks()


    def laser_collision(self):#method to detect collision between enemy laser and player 
        for laser in self.lasers:
            if pygame.sprite.spritecollide(game.player,self.lasers,True):
                game.player.health-=1
                self.lasers.remove(laser)
    
    def laser_delete(self):
        for laser in self.lasers:
            if laser.rect.centerx > SCREEN_WIDTH or laser.rect.centerx <=0:
                laser.kill()
            elif laser.rect.centery > SCREEN_HEIGHT or laser.rect.centery <=0:
                laser.kill()

class Bullet(pygame.sprite.Sprite): #bullet class inherits from sprite class
    def __init__(self, angle, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(
            "assets/bullet.png").convert_alpha(), (16, 16))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.angle = angle
        self.speed = 15

    def change(self): #method to move bullets towards the direction of the cursor
        self.rect.centery -= int(math.sin(self.angle) * self.speed) #sine used to calculate the change in y position 
        self.rect.centerx -= int(math.cos(self.angle) * self.speed) #cosine used to calculate the change in x position 
        
        #collision detection for bullets, if collides with the map borders will bounce off walls once 
        if self.rect.y <= 30 or self.rect.y >= 680:
            self.speed = -15 
        if self.rect.x <= 35 or self.rect.x >= 1220:
            self.speed = -15

class Target: #target class for cursor 
    def __init__(self, x, y, width, height):
        self.image = pygame.transform.scale(
            pygame.image.load("assets/cursor.png"), (width, height))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.width = width
        self.height = height

    def update(self): #method to move the cursor based on the position of the mouse 
        self.rect.center = pygame.mouse.get_pos()
        self.rect.x = self.rect.center[0] - self.width/2
        self.rect.y = self.rect.center[1] - self.height/2
        DISPLAY.blit(self.image, (self.rect.x, self.rect.y))

class Enemy_laser(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((8,8))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.speed = 5
    
    def move(self):
        self.rect.centery += math.cos(0) * self.speed
        self.rect.centerx += math.sin(0) * self.speed
        
class Game: #game class
    def __init__(self):
        self.enemies = pygame.sprite.Group() 
        self.player = Player() #player object instantiated inside game class (composition)
        self.target = Target(0, 0, 30, 30) #target object instantiated inside game class (composition)
        self.game_over = False 
        self.collision_tolerance = 10
        self.difficulty = 0 
        self.background = pygame.transform.scale(pygame.image.load(
            'assets/map.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def display_ui(self): 
        #method to display score, timer and player lives in game
        for i in range(self.player.max_health):
            img = pygame.image.load(
                "assets/heart_empty.png" if i >= self.player.health else "assets/heart.png")
            img = pygame.transform.scale(img, (50, 50))
            DISPLAY.blit(img, (i*50+WINDOWSIZE[0]/2-self.player.max_health*25, 25))

        score_text = TEXT_FONT.render(f'Score: {database.score}', True, (255, 255, 255))
        DISPLAY.blit(score_text, (score_text.get_width()/2, 25))

        time = (pygame.time.get_ticks()//1000) - start_time
        time_text = TEXT_FONT.render(f'Time: {time}', True, (255, 255, 255))
        DISPLAY.blit(time_text, (1000, 25))
        return time #returns the time calculated to be stored in database 

    def shoot(self):
        self.player.shoot()

    def update_screen(self):
        CLOCK.tick(60)
        pygame.display.update()

    def E_enemy_spawner_1(self): #enemy spawner for slime when easy mode is selected 
        while True:
            for i in range(80):
                yield
            randomx = random.randint(0, 1220)
            randomy = random.randint(20, 670)
            enemy = Slime(randomx, randomy,1) #composition of slime class
            while abs(self.player.rect.centerx-enemy.x) < 250 and abs(self.player.rect.centery-enemy.y)<250: #make sure that enemy doesn't spawn directly on player 
                enemy.x = random.randint(0-90,1220-90)
                enemy.y = random.randint(20-90,670-90)
            self.enemies.add(enemy)
            
    def E_enemy_spawner_2(self): #enemy spawner for skeleton1 when easy mode is selected 
        while True:
            for i in range(180):
                yield
            randomx = random.randint(0, 1220)
            randomy = random.randint(20, 670)
            enemy2 = Skeleton1(randomx,randomy,1) #composition of skeleton1
            while abs(self.player.rect.centerx-enemy2.x) < 250 and abs(self.player.rect.centery-enemy2.y)<250:
                enemy2.x = random.randint(0-90,1220-90)
                enemy2.y = random.randint(20-90,670-90)
            self.enemies.add(enemy2)

    def E_enemy_spawner_3(self): #spawner for skeleton2 when easy mode is selected 
        while True:
            for i in range(200):
                yield
            randomx = random.randint(10, 1100)
            randomy = random.randint(50,60)
            enemy3 = Skeleton2(randomx,randomy,0) #composition of skeleton2
            self.enemies.add(enemy3)

    def M_enemy_spawner_1(self): #spawner for slime when medium mode selected 
        while True:
            for i in range(60):
                yield
            randomx = random.randint(0, 1220)
            randomy = random.randint(20, 670)
            enemy = Slime(randomx,randomy,1) #composition of slime 
            while abs(self.player.rect.centerx-enemy.x) < 500 and abs(self.player.rect.centery-enemy.y)<500:
                enemy.x = random.randint(0,1220-90)
                enemy.y = random.randint(20,670-90)
            self.enemies.add(enemy)

    def M_enemy_spawner_2(self): #spawner for skeleton1 when medium mode selected
        while True:
            for i in range(160):
                yield
            randomx = random.randint(0, 1220)
            randomy = random.randint(20, 670)
            enemy2 = Skeleton1(randomx,randomy,2) #composition of skeleton1
            while abs(self.player.rect.centerx-enemy2.x) < 500 and abs(self.player.rect.centery-enemy2.y)<500:
                enemy2.x = random.randint(0,1220-90)
                enemy2.y = random.randint(20,670-90)
            self.enemies.add(enemy2)

    def M_enemy_spawner_3(self): #spawner for skeleton2 when medium mode selected 
        while True:
            for i in range(120):
                yield
            randomx = random.randint(10, 1100)
            randomy = random.randint(50,60)
            enemy3 = Skeleton2(randomx,randomy,0) #composition of skeleton2
            self.enemies.add(enemy3)

    def H_enemy_spawner_1(self): #spawner for slime when hard mode selected
        while True:
            for i in range(60):
                yield
            randomx = random.randint(0, 1220)
            randomy = random.randint(20, 670)
            enemy = Slime(randomx,randomy,2) #composition of slime 
            while abs(self.player.rect.centerx-enemy.x) < 500 and abs(self.player.rect.centery-enemy.y)<500:
                enemy.x = random.randint(0,1220-90)
                enemy.y = random.randint(20,670-90)
            self.enemies.add(enemy)

    def H_enemy_spawner_2(self): #spawner for skeleton1 when hard mode selected 
        while True:
            for i in range(100):
                yield
            randomx = random.randint(0, 1220)
            randomy = random.randint(20, 670)
            enemy2 = Skeleton1(randomx,randomy,2) #composition of skeleton1
            while abs(self.player.rect.centerx-enemy2.x) < 500 and abs(self.player.rect.centery-enemy2.y)<500:
                enemy2.x = random.randint(0,1220-90)
                enemy2.y = random.randint(20,670-90)
            self.enemies.add(enemy2)

    def H_enemy_spawner_3(self): #spawner for skeleton2 when hard mode selected
        while True:
            for i in range(200):
                yield
            randomx = random.randint(10, 1100)
            randomy = random.randint(50,60)
            enemy3 = Skeleton2(randomx,randomy,0) #skeleton2 composition
            self.enemies.add(enemy3)

    def draw(self): #method for updating and drawing all objects 
        self.target.update()
        self.player.update()
        self.player.bullets.update()

    def game_over_call(self): #method to display game over screen 
        pygame.mouse.set_visible(True)
        score_text = TEXT_FONT.render(f'Final Score: {database.score}', True, (255,255,255))
        DISPLAY.fill((0,0,0))
        DISPLAY.blit(score_text,(450,300))

        time_text = TEXT_FONT.render(f'Final Time: {database.time} Seconds', True, (255,255,255))
        quit_text = TEXT_FONT.render("Press X button in top right corner of window to quit game",True,(255,255,255))
        leaderboardtext = TEXT_FONT.render("Leaderboard and other info presented in terminal",True,(255,255,255))
        DISPLAY.blit(leaderboardtext,(100,600))
        DISPLAY.blit(time_text,(450,400))
        DISPLAY.blit(quit_text,(50,500))

        self.update_screen()


    def check_game_over(self): #method to check if the game has ended or not 
        if self.player.health <= 0:
            if self.game_over == False:
                self.game_over = True
            
    def enemy_player_collision(self): #collision detection between enemy sprite and player sprite, if enemy and player collide, player loses a heart and enemy sprite is removed from game 
        for e in self.enemies:
            e.update()
            if e.rect.colliderect(self.player.rect):
                if self.player.rect.top-e.rect.bottom < self.collision_tolerance:
                    self.enemies.remove(e)
                    self.player.health -= 1
                elif self.player.rect.bottom - e.rect.top < self.collision_tolerance:
                    self.enemies.remove(e)
                    self.player.health -= 1
                elif self.player.rect.right - e.rect.left < self.collision_tolerance:
                    self.enemies.remove(e)
                    self.player.health -= 1
                elif self.player.rect.left - e.rect.right < self.collision_tolerance:
                    self.enemies.remove(e)
                    self.player.health -= 1

    def draw_bullets(self): #draw and update all player bullets 
            if self.player.bullets:
                for b in self.player.bullets:
                    b.change()
                    self.player.bullets.draw(DISPLAY)

    def collision_enemy(self): #collision detection between player bullet sprites and enemy sprite, if bullets collide with enemies the bullet sprite is removed from game and enemy health decreases 
        for enemy in self.enemies:
            if pygame.sprite.spritecollide(enemy,self.player.bullets,True):
                enemy.health -= 1
                if enemy.health <=0:
                    database.score+=10
                    self.enemies.remove(enemy)

#instantiation of pygame object
pygame.init()


#constants 
TEXT_FONT = pygame.font.Font("assets/font.otf", 32)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WINDOWSIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
DISPLAY = pygame.display.set_mode(WINDOWSIZE)
CLOCK = pygame.time.Clock()

pygame.font.get_init()
pygame.display.set_caption("Desert Dungeons")

#game object and database object 
game = Game()
database = SQL("Data.db")
database.get_last_id()

#variables for spawners to be used in game loop 
Espawn1 = game.E_enemy_spawner_1()
Espawn2 = game.E_enemy_spawner_2()
Espawn3 = game.E_enemy_spawner_3()
Mspawn1 = game.M_enemy_spawner_1()
Mspawn2 = game.M_enemy_spawner_2()
Mspawn3 = game.M_enemy_spawner_3()
Hspawn1 = game.H_enemy_spawner_1()
Hspawn2 = game.H_enemy_spawner_2()
Hspawn3 = game.H_enemy_spawner_3()

#main game loop 
while True:
    for event in pygame.event.get():
        #close game when X is pressed in window 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #check for mouse button input to allow player to shoot bullets
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.player.shoot()

        else:
            #conditions to check which mode player selects in main menu 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                game.difficulty = 1
                game.player.health = 5
                game.player.max_health =5
                game_active = True
                start_time = int(pygame.time.get_ticks()//1000)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                game.difficulty = 2
                game.player.health = 4
                game.player.max_health = 4
                game_active = True
                start_time = int(pygame.time.get_ticks()//1000)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                game.difficulty = 3
                game.player.health = 3
                game.player.max_health = 3
                game_active = True
                start_time = int(pygame.time.get_ticks()//1000)

    #game loop when easy mode is selected
    if game_active and game.difficulty ==1:
        pygame.mouse.set_visible(False)
        DISPLAY.fill((0, 0, 0))
        DISPLAY.blit(game.background,(0,0))
        game.draw()
        game.draw_bullets()
        game.player.bullet_delete()
        next(Espawn1)
        next(Espawn2)
        next(Espawn3)
        if game.game_over:
            game.game_over_call()
            import leaderboardtimes
            continue
        game.enemy_player_collision()
        game.check_game_over()
        game.enemy_player_collision()
        game.collision_enemy()
        database.time = game.display_ui()
        database.add_to_database()
        
    #game loop when medium mode is selected 
    elif game_active and game.difficulty == 2:
        pygame.mouse.set_visible(False)
        DISPLAY.fill((0, 0, 0))
        DISPLAY.blit(game.background,(0,0))
        game.draw()
        game.draw_bullets()
        next(Mspawn1)
        next(Mspawn2)
        next(Mspawn3)
        if game.game_over:
            game.game_over_call()
            import leaderboardtimes
            continue 
        game.enemy_player_collision()
        game.check_game_over()
        game.enemy_player_collision()
        game.collision_enemy()
        database.time = game.display_ui()
        database.add_to_database()
        
    #game loop when hard mode is selected 
    elif game_active and game.difficulty == 3:
        pygame.mouse.set_visible(False)
        DISPLAY.fill((0, 0, 0))
        DISPLAY.blit(game.background,(0,0))
        game.draw()
        game.draw_bullets()
        next(Hspawn1)
        next(Hspawn2)
        next(Hspawn3)
        if game.game_over:
            game.game_over_call()
            import leaderboardtimes
            continue 
        game.enemy_player_collision()
        game.check_game_over()
        game.enemy_player_collision()
        game.collision_enemy()
        database.time = game.display_ui()
        database.add_to_database()
        
    #when the game ends, displays end game screen 
    else:
        pygame.mouse.set_visible(True)
        DISPLAY.fill((239,152,52))
        DISPLAY.blit(TEXT_FONT.render("DESERT DUNGEONS",True,(0,0,0)),(500,10))
        DISPLAY.blit(TEXT_FONT.render("WASD to move, mouse to aim, left click to shoot",True,(255,255,255)),(10,50))
        DISPLAY.blit(TEXT_FONT.render("Slime = 1 Health (1 hit to kill)",True,(255,255,255)),(10,100))
        DISPLAY.blit(TEXT_FONT.render("Normal skeleton = 2 health (2 hits to kill)",True,(255,255,255)),(10,150))
        DISPLAY.blit(TEXT_FONT.render("Purple skeleton = 3 health (3 hits to kill)",True,(255,255,255)),(10,200))
        DISPLAY.blit(TEXT_FONT.render("CHOOSE DIFFICULTY: 1(EASY), 2(MEDIUM), 3(HARD)",True,(0,0,0)),(10,500))
    
    game.update_screen()
    