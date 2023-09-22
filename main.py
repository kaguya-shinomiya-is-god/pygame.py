import pygame as pg
import random

pg.init()
playerImg = pg.image.load("pygame.py/player.png")
playerImg = pg.transform.scale(playerImg,(100,100))
bgImg = pg.image.load("pygame.py/bg.png")
enemyImg = pg.image.load("pygame.py/viruz.png")
enemyImg = pg.transform.scale(enemyImg,(100,100))
bulletImg = pg.image.load("pygame.py/projetil.png")
bulletImg = pg.transform.scale(bulletImg,(55,55))

screen = pg.display.set_mode((500,700))
clock = pg.time.Clock()
time = pg.time.get_ticks
enemyNumber = 0
running = True
sX = screen.get_width
sY = screen.get_height
dt = 0
shooting = False
ammo = 0
money = 0

bullets_removed = set()
enemies_removed = set()

class projectile(object):
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size
        self.hitbox = (self.x,self.y,10,10)
        self.rect = pg.Rect(self.x,self.y,10,10)
    def draw(self,win):
        #pg.draw.circle(win, "purple", (self.x,self.y), self.size)
        screen.blit(bulletImg,(self.x - 28,self.y - 35))
        self.hitbox = (self.x - 5, self.y - 5, 10, 10)
        self.rect = pg.Rect(self.x - 5, self.y - 5, 10, 10)
        pg.draw.rect(win, "white", self.hitbox,2)

class player(object):
    def __init__(self,x,y,size,spd):
        self.x = x
        self.y = y
        self.player_pos = pg.Vector2(x,y)
        self.size = size
        self.spd = spd
        self.hitbox = (self.x + 20, self.y, 60)
        self.hp = 0
    def drawn(self,win):
        #pg.draw.circle(screen, "green", (self.x,self.y), self.size)
        screen.blit(playerImg, (self.x - 50,self.y - 20))
        self.hitbox = (self.x - 40, self.y, 80, 80) 
        #pg.draw.rect(win, "white", self.hitbox,2)

    def moveFront(self):
        self.y -= self.spd * dt
    def moveBack(self):
        self.y += self.spd * dt
    def moveLeft(self):
        self.x -= self.spd * dt
    def moveRight(self):
        self.x += self.spd * dt

class enemy(object):
    def __init__(self,x,y,hp,size,spd,id):
        self.id = id
        self.x = x
        self.y = y
        self.hp = hp
        self.level = hp
        self.size = size
        self.spd = spd
        self.image = enemyImg
        self.hitbox = (self.x + 10, self.y, 30, 20)
        self.rect = pg.Rect(self.x + 10, self.y, 30, 20)

    def draw(self,win):
        self.move()
        #pg.draw.circle(screen, "red", (self.x,self.y), self.size * (self.hp/2))
        self.image = pg.transform.scale(self.image, (self.size * (self.hp/2) * 2,self.size * (self.hp/2) * 2))
        screen.blit(self.image,(self.x - 50,self.y - 50))

        self.hitbox = (self.x - 30, self.y - 30, 60, 60) # NEW
        self.rect = pg.Rect(self.x - 30, self.y - 30, 60, 60)
        #pg.draw.rect(win, "white", self.hitbox,2)

    def move(self):
        self.y += self.spd
    def getBox(self):
        return self.hitbox
    def hit(self):
        print("hit at " + str(enemyNumber) + "\n hp = " + str(self.hp))
        self.hp -= 0.05
        

score_font = pg.font.SysFont('monocraft', 32)

p1 = player(screen.get_width() / 2, screen.get_height() / 2,40,300)
bullets = []
enemies = []

while running:
    screen.blit(bgImg,(0,0))
    if ammo < -200:
        ammo = -200
    
    temp_enemy_hp = random.randint(1,3)

    bullets = [bullet for bullet in bullets if bullet not in bullets_removed]
    enemies = [enemie for enemie in enemies if enemie not in enemies_removed]

    pg.draw.rect(screen, "pink", pg.Rect(25, 450, 75, 200))
    pg.draw.rect(screen, "black", pg.Rect(25, 450, 75, 200),10)
    pg.draw.rect(screen, "black", pg.Rect(25, 450, 75, p1.hp))

    pg.draw.rect(screen, "yellow", pg.Rect(400, 450, 75, 200))
    pg.draw.rect(screen, "black", pg.Rect(400, 450, 75, 200),10)
    pg.draw.rect(screen, "black", pg.Rect(400, 450, 75, abs(ammo)))
    score_text = score_font.render("Score: " + str(money),True,"yellow")
    score_textRect = score_text.get_rect()
    score_textRect.center = (120, 40)
    
    for bullet in bullets:
        bullet.draw(screen)
    for enemie in enemies:
        enemie.draw(screen)

    for bullet in bullets:
        for enemie in enemies:
            collide = pg.Rect.colliderect(bullet.rect,enemie.rect)
            if collide:
                enemie.hit()
                bullets_removed.add(bullet)
            
    
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        p1.moveFront()
    if keys[pg.K_s]:
        p1.moveBack()
    if keys[pg.K_a]:
        p1.moveLeft()
    if keys[pg.K_d]:
        p1.moveRight()
    if (keys[pg.K_SPACE]):
        if(ammo > -200):
            bullets.append(projectile(round(p1.x), round(p1.y),6))
            ammo -= 1
            print(ammo)
        shooting = True
    else:
        shooting = False

    if random.randint(1,50) == 42:
        enemies.append(enemy(random.randrange(50,450), 0,temp_enemy_hp,30,2,enemyNumber))
        enemyNumber += 1
        if ammo < 0:
            ammo += 30 * temp_enemy_hp

    for bullet in bullets:
        if bullet.y < 800 and bullet.y > 0:
            bullet.y -= 8
        else:
            bullets_removed.add(bullet)

    for enemie in enemies:
        if enemie.hp < 0.5:
            enemies_removed.add(enemie)
            print("Enemy " + str(enemie.id) + " killed")
            money += 20 * enemie.level
        if enemie.y > 800:
            enemies_removed.add(enemie)
            p1.hp += enemie.hp * 5
            print("Damage!, Hp = " + str(p1.hp))

    p1.drawn(screen)
    screen.blit(score_text, score_textRect)
    pg.display.flip()
    dt = clock.tick(60) / 1000

    if p1.hp >= 200:
        running = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()