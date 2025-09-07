import random
import math
import pygame
from pygame import mixer
pygame.init()
# display
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invidars", "spaceship.png")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
# player info
player = pygame.image.load("space.png")
playerx = 260
playery = 555
playerx_change = 0
# enemy info
#we  have created list so that we can have multiple enemies in it:
enemy=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
enemiesno=6

for i in range(enemiesno):
 enemy.append(pygame.image.load("game.png"))
 enemyx.append(random.randint(0, 375))
 enemyy.append(random.randint(0, 375))
 enemyx_change.append(0.2)
 enemyy_change.append(10)

# bullet info
# ready means u cant see bullet on the screen
# fire means bullet is currently moving
bullet = pygame.image.load("bullet.png")
bulletx = 0
bullety = 555
bulletx_change = 0
bullety_change =1
bullet_state = "ready"

#creation of score card on display
score_v=0
font=pygame.font.Font("freesansbold.ttf",32)
testX=10
testY=10

game_over=pygame.font.Font("freesansbold.ttf",64)

# background image and music
back = pygame.image.load("bg.jpg")
mixer.music.load("background.wav")
mixer.music.play(-1)



# function creation of player and enemy
def player1(x, y):
    screen.blit(player, (x, y))


def enemy1(x, y,i):
    screen.blit(enemy[i], (x, y))

#function creation of bullet firing
def bullet1(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))

def game_over_text():

    over_text=game_over.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(111,250))
#function creation for collision
def iscollision(enemyx,enemyy,bulletx,bullety):
    distance=math.sqrt((math.pow(enemyx-bulletx,2))+(math.pow(enemyy-bullety,2)))
    if distance<27:
        return True
    else:
        return False

#function creation for score_card:
def show_score(x,y):
    score=font.render("Score :"+str(score_v),True,(255,255,255))
    screen.blit(score,(x,y))
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    screen.blit(back, (0, 0))
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                playerx_change = -0.9
            if i.key == pygame.K_RIGHT:
                playerx_change = +0.9
            if i.key== pygame.K_SPACE:
                if bullet_state=="ready":
                 bullet_sound=mixer.Sound("laser.wav")
                 bullet_sound.play()
                 bulletx=playerx
                 bullet1(bulletx,bullety)
        if i.type == pygame.KEYUP:
            if i.key == pygame.K_LEFT or i.key == pygame.K_RIGHT:
                playerx_change = 0


    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    if playerx >= 575:
        playerx = 575

    #ENEMY MOVEMENT
    for i in range(enemiesno):

      if enemyy[i]>500:
          for j in range(enemiesno):
              enemyy[j]=2000
          game_over_text()
          break
      enemyx[i] += enemyx_change[i]
      if enemyx[i] <= 0:
        enemyx_change[i]= +0.3
        enemyy[i] += enemyy_change[i]
      elif enemyx[i] >= 575:
        enemyx_change[i] = -0.3
        enemyy [i]+= enemyy_change[i]

      collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
      if collision:
          explo_sound=mixer.Sound("explosion.wav")
          explo_sound.play()
          bullety = 555
          bullet_state = "ready"
          score_v += 1
          enemyx[i] = random.randint(0, 575)
          enemyy[i] = random.randint(0, 575)
      enemy1(enemyx[i], enemyy[i],i)






    #Bullet Movement
    #to fire multiple bullets we usedthe bullety<=0 then again reset it on y=555 and bullet_stateto ready
    if bullety<=0:
        bullety=555
        bullet_state="ready"
    if bullet_state =="fire":
        bullet1(bulletx,bullety)
        bullety -=bullety_change






    show_score(testX,testY)
    player1(playerx, playery)
    pygame.display.update()
