import pygame
import math
import random 
from pygame import mixer 


def background_choose():
    try:
        back=int(input('''which Background you want ?
                            1.anime space theme
                            2.normal version 
choose one of them : '''))
        if back == 1 :
            print('Welcome to the game!')
            return 'background2.png'
        else :
            print('Welcome to the game!')
            return 'background1.png'
    except:
        print('Welcome to the game!')
        return 'background1.png'
# if any error  happen in choosing background then defult background will run .
       
choose_back=background_choose()


# initilization the pygame 
pygame.init()

# creating the screen 
screen= pygame.display.set_mode((800,600)) # (x,y) in 4th quadrants

# background 
#backImg1= pygame.image.load('background1.png')
#backImg2= pygame.image.load('background2.png')
backImg= pygame.image.load(choose_back)

# backgorund sound
mixer.music.load('sb_indreams.mp3')
mixer.music.play(-1)

# caption & icon 
pygame.display.set_caption("Space Invader")
icon= pygame.image.load('logo.png')  
pygame.display.set_icon(icon) 

# if the image does not load, check the current dir(os.getcwd) and move the image png there .

# player 
playerImg= pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0

# enemy 
em=['enemy1.png','enemy2.png','enemy3.png']
enemyImg= []
enemyX= []
enemyY= []
enemyX_change=[]
enemyY_change=[]
num_of_enemy=random.randint(3,6)

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load(random.choice(em)))
    enemyX.append(random.randint(0,740))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# bullet 
# ready - not visisble on screen 
# fire - visible on screen
bulletImg= pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=1
bullet_state='ready'

# score
score_value=0
front=pygame.font.Font('StreetFlowNYC.otf',32)

textX=10
textY=10

# gave over 
over_font=pygame.font.Font('StreetFlowNYC.otf',64)

def show_score(x,y):
    score= front.render(f'Score : {str(score_value)} ',True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_game= over_font.render('GAME OVER!',True,(255,255,255))
    screen.blit(over_game,(220,250))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(emX,emY,buX,buY):
    dist= math.sqrt((math.pow(emX-buX,2))+(math.pow(emY-buY,2)))
    if dist< 27:
        return True
    else:
        return False

# game loop 
running = True 
while running:

    # screen color , RGB - red green blue
    screen.fill((0,0,0)) 
    screen.blit(backImg,(0,0)) 

    # playerX += 0.2
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False

    # if key pressed check is it right or left 
        if event.type== pygame.KEYDOWN:
            if event.key== pygame.K_LEFT:
                playerX_change = -0.5
            if event.key== pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE or  event.key == pygame.K_b or  event.key == pygame.K_q or event.key == pygame.K_UP:
                if bullet_state is 'ready':
                    bullet_sound=mixer.Sound('fire.mp3')
                    bullet_sound.play()
                    # get the current x on screen 
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
            

        
        if event.type == pygame.KEYUP:
            if event.key== pygame.K_LEFT or event.key== pygame.K_RIGHT: 
                playerX_change=0
        

        

        

    # player boundery
    playerX += playerX_change

    if playerX <= 0 :
        playerX= 0
    elif playerX >= 736:
        playerX= 736

    # enemy boundery

    for i in range(num_of_enemy):

        # game over 
        if enemyY[i]>460:
            for j in range(num_of_enemy):
                enemyY[j]=2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0 :
            enemyX_change[i]= 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]= -0.5
            enemyY[i] += enemyY_change[i]

        # collision 
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound=mixer.Sound('hit.mp3')
            explosion_sound.play()
            bulletY=480
            bullet_state='ready'
            score_value +=1
            random.shuffle(em)
            enemyImg[i]= pygame.image.load(random.choice(em))
            enemyX[i]=random.randint(0,740)
            enemyY[i]=random.randint(50,150)


        enemy(enemyX[i],enemyY[i],i)
        
        


    # bullet movement
    if bulletY <=0 :
        bulletY=480
        bullet_state='ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY = bulletY - bulletY_change
    
    player(playerX,playerY)
    show_score(textX,textY)

    pygame.display.update()
