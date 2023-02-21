import pygame
import sys
import math
import random
import sqlite3


class SQL:
    def __init__(self,database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        self.score = 0
        self.time = 0
        self.id = self.cur.execute("SELECT AttemptID FROM LoggedIn").fetchall()
        self.all_id = []

    def add_to_database(self):
        update_query = """UPDATE LoggedIn SET Score = ? , Time = ? WHERE AttemptID = ?"""
        data = (self.score,self.time,self.id)
        self.cur.execute(update_query,data)
        self.conn.commit()
        
    def get_last_id(self):
        for id in self.id:
            self.all_id.append(int(id[0]))
        self.all_id.sort()
        self.id = self.all_id[-1]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = self.max_health = 3
        self.image = pygame.transform.scale(pygame.image.load(
            "assets/test.png").convert_alpha(), (40, 40))
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
        self.animations = {"up": [pygame.transform.scale(pygame.image.load("assets/player sprite/tile006.png").convert_alpha(), (40, 40)), pygame.transform.scale(pygame.image.load("assets/player sprite/tile007.png").convert_alpha(), (40, 40)),
                                  pygame.transform.scale(pygame.image.load("assets/player sprite/tile008.png").convert_alpha(), (40, 40))],
                           "down": [pygame.transform.scale(pygame.image.load("assets/player sprite/tile001.png").convert_alpha(), (40, 40)),
                                    pygame.transform.scale(pygame.image.load("assets/player sprite/tile002.png").convert_alpha(), (40, 40))],
                           "right": [pygame.transform.scale(pygame.image.load("assets/player sprite/tile003.png").convert_alpha(), (40, 40)), pygame.transform.scale(pygame.image.load("assets/player sprite/tile004.png").convert_alpha(), (40, 40)),
                                     pygame.transform.scale(pygame.image.load("assets/player sprite/tile005.png").convert_alpha(), (40, 40))],
                           "left": [pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile003.png").convert_alpha(), True, False), (40, 40)), pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile004.png").convert_alpha(), True, False), (40, 40)),
                                    pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player sprite/tile005.png").convert_alpha(), True, False), (40, 40))],
                           "idle": [pygame.transform.scale(pygame.image.load("assets/player sprite/tile000.png").convert_alpha(), (40, 40))]}

    def input(self):
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
            print("shoot")
            self.shoot()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.centerx += self.direction.x * speed
        self.rect.centery += self.direction.y * speed
        if self.rect.right >= 1220:
            self.rect.right = 1220
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.bottom >= 670:
            self.rect.bottom = 670
        if self.rect.top <= 20:
            self.rect.top = 20

    def get_status(self):

        if self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]

        self.frame_count += self.animation_speed
        if self.frame_count >= len(animation):
            self.frame_count = 0

        self.image = animation[int(self.frame_count)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(
            (self.rect.centery-mouse_pos[1]), (self.rect.centerx-mouse_pos[0]))
        self.bullets.add(Bullet(angle, self.rect.centerx, self.rect.centery))

    def update(self):
        
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
        DISPLAY.blit(self.image,(self.rect.centerx,self.rect.centery))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y,speed):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):

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

class Slime(Enemy):
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

class Skelly1(Enemy):
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

class Skelly2(Enemy):
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            "assets/bullet.png").convert_alpha(), (16, 16))
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 15

    def change(self):
        self.rect.centery -= int(math.sin(self.angle) * self.speed)
        self.rect.centerx -= int(math.cos(self.angle) * self.speed)
        if self.rect.y <= -50 or self.rect.y >= SCREEN_HEIGHT + 50:
            self.speed = -15

        if self.rect.x <= -50 or self.rect.x >= SCREEN_WIDTH + 50:
            self.speed = -15

class Target:
    def __init__(self, x, y, width, height):
        self.image = pygame.transform.scale(
            pygame.image.load("assets/cursor.png"), (width, height))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.width = width
        self.height = height

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.rect.x = self.rect.center[0] - self.width/2
        self.rect.y = self.rect.center[1] - self.height/2
        DISPLAY.blit(self.image, (self.rect.x, self.rect.y))

class Game:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.player = Player()
        self.target = Target(0, 0, 30, 30)
        self.game_over = False
        self.collision_tolerance = 10

    def display_ui(self):
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
        return time

    def shoot(self):
        print("shoot")
        self.player.shoot()

    def update_screen(self):
        CLOCK.tick(60)
        pygame.display.update()

    def enemy_spawner_1(self):
        while True:
            for i in range(55):
                yield
            randomx = random.randint(0, 1220)
            randomy = random.randint(20, 670)
            enemy = Slime(randomx, randomy,2)
            self.enemies.add(enemy)
            
    def enemy_spawner_2(self):
        while True:
            for i in range(150):
                yield
            randomx = random.randint(0, 1220)
            randomy = random.randint(20, 670)
            enemy2 = Skelly1(randomx,randomy,2)
            self.enemies.add(enemy2)

    def enemy_spawner_3(self):
        while True:
            for i in range(360):
                yield
            randomx = random.randint(0, 1220)
            randomy = random.randint(20, 670)
            enemy3 = Skelly2(randomx,randomy,3)
            self.enemies.add(enemy3)

    def draw(self):
        self.target.update()
        self.player.update()
        self.player.bullets.update()

    def game_over_call(self):
        pygame.mouse.set_visible(True)
        score_text = TEXT_FONT.render(f'Final Score: {database.score}', True, (255,255,255))
        DISPLAY.fill((0,0,0))
        DISPLAY.blit(score_text,(450,300))

        time_text = TEXT_FONT.render(f'Final Time: {database.time} Seconds', True, (255,255,255))
        DISPLAY.blit(time_text,(450,400))
        self.update_screen()

    def check_game_over(self):
        if self.player.health <= 0:
            if self.game_over == False:
                self.game_over = True
            
    def enemy_player_collision(self):
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

    def draw_bullets(self):
            if self.player.bullets:
                for b in self.player.bullets:
                    b.change()
                    self.player.bullets.draw(DISPLAY)

pygame.init()
pygame.font.get_init()

TEXT_FONT = pygame.font.Font("assets/font.otf", 32)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WINDOWSIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

DISPLAY = pygame.display.set_mode(WINDOWSIZE)
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Grave Fighter")

game = Game()
database = SQL("Data.db")
database.get_last_id()

game_active = False
spawn1 = game.enemy_spawner_1()
spawn2 = game.enemy_spawner_2()
spawn3 = game.enemy_spawner_3()

BACKGROUND = pygame.transform.scale(pygame.image.load(
            'assets/map.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.player.shoot()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()//1000)
    
    if game_active:
        pygame.mouse.set_visible(False)
        DISPLAY.fill((0, 0, 0))
        DISPLAY.blit(BACKGROUND,(0,0))
        game.draw()
        game.draw_bullets()

        if game.game_over:
            game.game_over_call()
            continue
        
        next(spawn1)
        next(spawn2)
        next(spawn3)

        game.enemy_player_collision()
        game.check_game_over()
        game.enemy_player_collision()
        
        for enemy in game.enemies:
            if pygame.sprite.spritecollide(enemy,game.player.bullets,True):
                enemy.health -= 1
                if enemy.health <=0:
                    database.score+=10
                    game.enemies.remove(enemy)
                            
        database.time = game.display_ui()
        
        database.add_to_database()
    
    else:
        pygame.mouse.set_visible(True)
        DISPLAY.fill((94,129,162))
        DISPLAY.blit(TEXT_FONT.render("WASD to move, mouse to aim, left click to shoot",True,(255,255,255)),(10,10))
        DISPLAY.blit(TEXT_FONT.render("Slime = 1 Health (1 hit to kill)",True,(255,255,255)),(10,100))
        DISPLAY.blit(TEXT_FONT.render("Normal skeleton = 2 health (2 hits to kill)",True,(255,255,255)),(10,150))
        DISPLAY.blit(TEXT_FONT.render("Purple skeleton = 3 health (3 hits to kill)",True,(255,255,255)),(10,200))
        DISPLAY.blit(TEXT_FONT.render("PRESS SPACE TO START",True,(255,255,255)),(10,500))
    game.update_screen()
    