import pygame
from pygame.locals import *
from random import randint
import os
import sys

# Hier wird der Pfad zum Verzeichnis der Assets gesetzt
DATAPATH = os.path.join(os.getcwd(), "data")

# Konstanten deklarieren
WIDTH, HEIGHT = 720, 520
BG_WIDTH = 1664
TITLE = "Pizza Plane Stage 2: Pizza, Pizza!"
FPS = 60
ANIM = 4 # Animation cycle
UPDOWN = 3
NO_ENEMIES = 10

# Farben
BG_COLOR = (231, 229, 226) # Wüstenhimmel

# Objekte
class Background(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.x = _x
        self.y = _y
        self.start_x = _x
        self.image = pygame.image.load(os.path.join(DATAPATH, "desert.png"))
        self.rect = self.image.get_rect()
        
    def update(self):
        self.x -= 1
        # print(self.x)
        self.rect.x = self.x
        if self.x <= -BG_WIDTH:
            self.x = BG_WIDTH

class Missile(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DATAPATH, "missile.png"))
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.speed = 10
        
    def update(self):
        self.rect.x += self.speed
        for enemy in enemies:
            if pygame.sprite.collide_rect(enemy, self):
                self.kill()
                # enemy.kill()
                e_x, e_y = enemy.rect.x, enemy.rect.y - 5
                enemy.reset()
                hit = Explosion(e_x, e_y)
                all_sprites.add(hit)
        if self.rect.x >= WIDTH + 20:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DATAPATH, "explosion.png"))
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.timer = 5
        
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()        

class  Plane(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load Images
        self.images = []
        for i in range (3):
            img = pygame.image.load(os.path.join(DATAPATH, "planered_" + str(i) + ".png"))
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.x = 75
        self.y = 250
        self.frame = 0
        self.ani = 20
        self.dir = "NONE"
        self.firecount = 0
    
    def update(self):
        if self.dir == "NONE":
            self.y += 0
        elif self.dir == "UP":
            if self.y > 20:
                self.y -= UPDOWN
        elif self.dir == "DOWN":
            if self.y < HEIGHT - 20:
                self.y += UPDOWN
        self.rect.center = (self.x, self.y)
        self.ani += 1
        if self.ani >= ANIM:
            self.ani = 0
            self.frame += 1
            if self.frame > 2:
                self.frame = 0
        self.firecount -= 1
        self.image = self.images[self.frame]
        
    def fire(self):
        if self.firecount < 0:
            missile = Missile(self.x + 15, self.y)
            all_sprites.add(missile)
            self.firecount = 15

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DATAPATH, "pizza.png"))
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.speed = randint(3, 6)
        
    def reset(self):
        self.rect.x = WIDTH + randint(30, 100)
        self.rect.y = randint(30, HEIGHT - 30)
        self.speed = randint(3, 6)
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -30:
            self.reset()
        

        
# Pygame initialisieren und das Fenster und die Hintergrundfarbe festlegen
clock = pygame.time.Clock()
pygame.init()
# Ein übler Hack, um die Position des Fensters auf meinen zweiten Bildschirm zu setzen,
# aber er funktioniert …
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1320, 60)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Sprite-Gruppe(n)
backs       = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemies     = pygame.sprite.Group()

# Hintergrund
back1 = Background(0, 0)
back2 = Background(BG_WIDTH, 0)
backs.add(back1)
backs.add(back2)

# Die Gegner
for _ in range(NO_ENEMIES):
    pizza = Enemy(WIDTH + randint(30, 100), randint(30, HEIGHT - 30))
    all_sprites.add(pizza)
    enemies.add(pizza)

# Der rote Flieger
plane = Plane()
all_sprites.add(plane)

keep_going = True
while keep_going:
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT)
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            print("Bye, Bye, Baby!")
            pygame.quit()
            try:
                sys.exit()
            finally:
                keep_going = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                plane.dir = "UP"
            elif event.key == pygame.K_DOWN:
                plane.dir = "DOWN"
            if event.key == pygame.K_RIGHT:
                plane.fire()
                
        if event.type == pygame.KEYUP:
            plane.dir = "NONE"

    backs.update()
    backs.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.update()
    pygame.display.flip()
