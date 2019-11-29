import pygame
import random
import math
import time
from pygame import mixer

pygame.init()

# Setting window dimensions.
screen = pygame.display.set_mode((800, 500))

# Adding title and icon
pygame.display.set_caption("Ever Wing")
icon = pygame.image.load('ufo.png')     
pygame.display.set_icon(icon)           # This is not showing the effect in linux.
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (800, 500))
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
player_img = pygame.image.load('player1.png')
playerX = 370
playerY = 400
playerX_change = 0

# Enemies
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (64, 64))
enemy_speed = 2
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 5
for i in range(num_of_enemy):
    enemyX.append(random.randint(50, 675))
    enemyY.append(random.randint(50, 125))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(30)

# Bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 400
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font('Mounting.ttf', 20)
posX = 0
posY = 0

# Display score
def show_score(x, y):
    score_font = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_font, (0, 0))

# Draw player
def player(x, y):
    if score < 50:
        player_img = pygame.image.load('player1.png')
    elif score < 100:
        player_img = pygame.image.load('player2.png')
    else:
        player_img = pygame.image.load('player3.png')
    screen.blit(player_img, (x, y))

# Draw enemy
def enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Draw bullet
def fire(x, y):
    global bullet_state
    bullet_state = "firing"
    screen.blit(bullet_img, (x+16, y+10))

# Find whether bullet attacks enemy
def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    if distance < 30:
        return True
    else:
        return False

# Loop for the game
run = True
while run:
    #screen.fill((0,200,100))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX < 30:
        playerX = 30
    if playerX > 700:
        playerX = 700
    
    for i in range(num_of_enemy):
        if enemyY[i] > 350:
            run = False
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 50:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        if enemyX[i] > 675:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]

        col = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if col:
            col_sound = mixer.Sound('explosion.wav')
            col_sound.play()
            bulletY = 400
            bullet_state = "ready"
            score += 5
            enemyX[i] = random.randint(50, 675)
            enemyY[i] = random.randint(50, 125)
            
        enemy(enemyX[i], enemyY[i])


    if bulletY <= 0:
        bulletY = 400
        bullet_state = "ready"

    if bullet_state is "firing":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(posX, posY)
    pygame.display.update()

font = pygame.font.Font('Mounting.ttf', 50)
end_font = font.render("-: GAME OVER :-", True, (255, 255, 255))
screen.blit(end_font, (150, 200))
pygame.display.update()
time.sleep(10)