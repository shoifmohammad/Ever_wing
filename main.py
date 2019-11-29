import pygame
import random
import math
import time
from pygame import mixer

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

sky = (0, 200, 100)
magenta = (128, 0, 128)
pink = (255, 20, 145)

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

# Draw rectangle.
def draw_rect(x, y, width, height, color):
    pygame.draw.rect(screen, color, [x, y, width, height])

low = 0
high = 0

def game_intro():
    global low
    global high

    # Choosing difficulty level.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        screen.fill(sky)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        text = pygame.font.Font("freesansbold.ttf", 40)
        text_font = text.render("Choose Difficulty Level", True, black)
        screen.blit(text_font, (175, 50))
        text = pygame.font.Font("freesansbold.ttf", 20)
        
        if 300 < mouse[0] < 500 and 150 < mouse[1] < 200:
            draw_rect(300, 150, 200, 50, pink)
            if click[0] == 1:
                low = 3
                high = 5
                return()
        else:
            draw_rect(300, 150, 200, 50, magenta)
        text_font = text.render("Easy", True, black)
        screen.blit(text_font, (375, 165))
        
        if 300 < mouse[0] < 500 and 250 < mouse[1] < 300:
            draw_rect(300, 250, 200, 50, pink)
            if click[0] == 1:
                low = 5
                high = 10
                return()
        else:
            draw_rect(300, 250, 200, 50, magenta)
        text_font = text.render("Moderate", True, black)
        screen.blit(text_font, (355, 265))
        
        if 300 < mouse[0] < 500 and 350 < mouse[1] < 400:
            draw_rect(300, 350, 200, 50, pink)
            if click[0] == 1:
                low = 10
                high = 20
                return()
        else:
            draw_rect(300, 350, 200, 50, magenta)
        text_font = text.render("Difficult", True, black)
        screen.blit(text_font, (360, 365))

        pygame.display.update()
        

game_intro()

# Player
player_img = pygame.image.load('player1.png')
playerX = 370
playerY = 400
playerX_change = 0
player_change = 5

# Enemies
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (64, 64))
enemy_speed = 3
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
if low < 5:
    num_of_enemy = 5
elif low < 10:
    num_of_enemy = 8
else:
    num_of_enemy = 10
for i in range(num_of_enemy):
    enemyX.append(random.randint(50, 675))
    enemyY.append(random.randint(50, 125))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(30)

# Bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = []
bulletY = []
bullet = 400
bulletX_change = 0
bulletY_change = 5
num_of_bullets = 0

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
    if score < 100:
        player_img = pygame.image.load('player1.png')
    elif score < 300:
        player_img = pygame.image.load('player2.png')
    else:
        player_img = pygame.image.load('player3.png')
    screen.blit(player_img, (x, y))

# Draw enemy
def enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Draw bullet
def fire(x, y):
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
            #run = False
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_change
            if event.key == pygame.K_RIGHT:
                playerX_change = player_change
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                if score < 100 :
                    bulletX.append(playerX)
                    bulletY.append(bullet)
                    fire(playerX, bullet)
                    num_of_bullets += 1
                elif score < 300 :
                    bulletX.append(playerX - 16)
                    bulletX.append(playerX + 16)
                    bulletY.append(bullet)
                    bulletY.append(bullet)
                    fire(playerX - 16, bullet)
                    fire(playerX + 16, bullet)
                    num_of_bullets += 2
                else:
                    bulletX.append(playerX - 16)
                    bulletX.append(playerX)
                    bulletX.append(playerX + 16)
                    bulletY.append(bullet)
                    bulletY.append(bullet)
                    bulletY.append(bullet)
                    fire(playerX - 16, bullet)
                    fire(playerX, bullet)
                    fire(playerX + 16, bullet)
                    num_of_bullets += 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX < 30:
        playerX = 30
    if playerX > 700:
        playerX = 700
    
    temp = []

    for i in range(num_of_enemy):
        if enemyY[i] > 350:
            run = False
            break
        
        if enemyX_change[i] > 0:
            enemyX_change[i] = random.randint(low, high)
        else:
            enemyX_change[i] = 0-random.randint(low, high)
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 50:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        if enemyX[i] > 675:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]
        for j in range(num_of_bullets):
            col = collision(enemyX[i], enemyY[i], bulletX[j], bulletY[j])
            if col:
                col_sound = mixer.Sound('explosion.wav')
                col_sound.play()
                temp.append(j)
                score += 5
                enemyX[i] = random.randint(50, 675)
                enemyY[i] = random.randint(50, 125)
                
        enemy(enemyX[i], enemyY[i])

    for i in range(len(temp)):
        del bulletX[i]
        del bulletY[i]
        num_of_bullets -= 1

    for i in range(num_of_bullets):
        if(bulletY[i] > 30):
            fire(bulletX[i], bulletY[i])
            bulletY[i] -= bulletY_change

    player(playerX, playerY)
    show_score(posX, posY)
    pygame.display.update()

font = pygame.font.Font('Mounting.ttf', 50)
end_font = font.render("-: GAME OVER :-", True, (255, 255, 255))
screen.blit(end_font, (150, 200))
pygame.display.update()
time.sleep(5)
pygame.quit()
quit()
