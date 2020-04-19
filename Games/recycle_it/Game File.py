import pygame
from pygame import mixer
import random
import time
import math
import sys

sys.path.append("../")
from head_controller import Head_comm

controller = Head_comm("Recycle It or Not!")

# Initialize pygame
pygame.init()

# Screen Size (x,y)
screen = pygame.display.set_mode((926, 634))

# Background
background = pygame.image.load('gamebkg.png')
game_lst = pygame.image.load('gameLostBkg.png')
game_wn = pygame.image.load('gameWonBkg.png')
menu = pygame.image.load('menubkg.png')
helps = pygame.image.load('helpbkg.png')

# Buttons
playb = pygame.image.load('play.png')
helpb = pygame.image.load('help.png')
exitb = pygame.image.load('exit.png')
lvl1 = pygame.image.load('lvl1.png')
lvl2 = pygame.image.load('lvl2.png')
lvl3 = pygame.image.load('lvl3.png')

# Background Music
mixer.music.load('backgroundmsc.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Recycle It or Not!")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Score
points_value = 0
font = pygame.font.Font('Bubblegum.ttf', 32)
textX = 10
textY = 10

# Number of enemies and good objects at any given time
num_of_each = 3

# Player + Starting Coordinates
playerImg = pygame.image.load('character_bin.png')
playerX = 463
playerY = 550
playerX_change = 0

# enemy -- non-recyclables
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
for i in range(num_of_each):
    # choosing which enemy to show
    enemySelect = random.randint(1, 5)
    if enemySelect == 1:
        enemyImg.append(pygame.image.load('enemy_banana.png'))
    if enemySelect == 2:
        enemyImg.append(pygame.image.load('enemy_core.png'))
    if enemySelect == 3:
        enemyImg.append(pygame.image.load('enemy_trash.png'))
    if enemySelect == 4:
        enemyImg.append(pygame.image.load('plastic6.png'))
    if enemySelect == 5:
        enemyImg.append(pygame.image.load('plastic3.png'))
    # random spawn location of enemy
    enemyX.append(random.randint(0, 862))
    enemyY.append(random.randint(0, 200) - 100)
    # speed of fall
    enemyY_change.append(2)

# good -- recyclable
goodX = []
goodY = []
goodY_change = []
goodImg = []

for i in range(num_of_each):
    # choosing which good object to show
    goodSelect = random.randint(1, 4)
    if goodSelect == 1:
        goodImg.append(pygame.image.load('good_bag.png'))
    if goodSelect == 2:
        goodImg.append(pygame.image.load('good_soda.png'))
    if goodSelect == 3:
        goodImg.append(pygame.image.load('plastic1.png'))
    if goodSelect == 4:
        goodImg.append(pygame.image.load('plastic2.png'))
    # random spawn of good object
    goodX.append(random.randint(0, 862))
    goodY.append(random.randint(0, 200) - 100)
    # speed of fall
    goodY_change.append(2)

# timer + level
clock = pygame.time.Clock()
seconds = 0
milliseconds = 0

level = 0


# Creating Player/Enemy/Good Object on-screen
# Enemy and Good Object have third unused parameter for selection of enemy/object picture
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def good(x, y, i):
    screen.blit(goodImg[i], (x, y))


def show_score(pts, x, y):
    score = font.render("Score: " + str(pts), True, (0, 0, 0))
    screen.blit(score, (x, y))


# Checking Collision by using distance formula between objects
# parameter is named var because function can be used by enemies and good objects
def isCollision(varX, varY, playerX, playerY):
    distance = math.sqrt((math.pow(varX - playerX, 2)) + (math.pow(varY - playerY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over(pts):
    if level == 0:
        if pts >= 1000:
            game_won(pts)
        else:
            game_lost(pts)
    if level == 1:
        if pts >= 1200:
            game_won(pts)
        else:
            game_lost(pts)
    if level == 2:
        if pts >= 1500:
            game_won(pts)
        else:
            game_lost(pts)


def game_won(pts):
    face = random.randint(1, 3)  # HEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRREEEEEEEEEEEEEE
    controller.face_update(face)
    # These commands won't over write themselves right? like if i say these three in a row
    # it'll hit all of the positions before going back to [90,90]?
    controller.head_update([90, 45])
    controller.head_update([90, 135])
    controller.head_update([90, 90])
    for i in range(num_of_each):
        enemyY[i] = 2000
        goodY[i] = 2000
        enemy(enemyX[i], enemyY[i], i)
        good(goodX[i], goodY[i], i)

    mixer.music.load('game_won.wav')
    mixer.music.play()
    pause = True
    while pause:
        screen.fill((255, 255, 255))
        screen.blit(game_wn, (0, 0))
        show_score(pts, 410, 200)
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    level_select(level)
                if event.key == pygame.K_SPACE:
                    pts = 0
                    game(playerX, points_value, playerX_change, milliseconds, seconds, level)
        pygame.display.update()


def game_lost(pts):
    face = random.randint(5, 7)  # HHHHHHHHHHHHHHEEEEEEEEEEEEERRRRRRRRRRRREEEEEEEEEEEE
    controller.face_update(face)
    #See game_won head update comments
    controller.head_update([45, 90])
    controller.head_update([135, 90])
    controller.head_update([90, 90])
    for i in range(num_of_each):
        enemyY[i] = 2000
        goodY[i] = 2000
        enemy(enemyX[i], enemyY[i], i)
        good(goodX[i], goodY[i], i)

    mixer.music.load('game_lose.wav')
    mixer.music.play()
    pause = True
    while pause:
        screen.fill((255, 255, 255))
        screen.blit(game_lst, (0, 0))
        show_score(pts, 410, 250)
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    level_select(level)
                if event.key == pygame.K_SPACE:
                    pts = 0
                    game(playerX, points_value, playerX_change, milliseconds, seconds, level)
        pygame.display.update()


def intro():
    bmenu = True
    controller.face_update(4)  # HEEEEEEEEEEEEEERRRREEEEEEEEEEEEE
    while bmenu:
        screen.fill((255, 255, 255))
        screen.blit(menu, (0, 0))
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(click)
        if 360 + 220 > mouse[0] > 360 and 80 + 70 > mouse[1] > 80:
            if click[0] == 1:
                level_select(level)
        else:
            screen.blit(playb, (360, 80))
        if 360 + 220 > mouse[0] > 360 and 170 + 70 > mouse[1] > 170:
            if click[0] == 1:
                help_screen()
        else:
            screen.blit(helpb, (360, 170))
        if 360 + 220 > mouse[0] > 360 and 260 + 70 > mouse[1] > 260:
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            screen.blit(exitb, (360, 260))

        pygame.display.update()


def ready():
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    ready = font.render("Ready ", True, (0, 0, 0))
    screen.blit(ready, (410, 200))
    pygame.display.update()
    pygame.time.delay(750)
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    ready = font.render("Ready. ", True, (0, 0, 0))
    screen.blit(ready, (410, 200))
    pygame.display.update()
    pygame.time.delay(750)
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    ready = font.render("Ready.. ", True, (0, 0, 0))
    screen.blit(ready, (410, 200))
    pygame.display.update()
    pygame.time.delay(750)
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    ready = font.render("Ready... ", True, (0, 0, 0))
    screen.blit(ready, (410, 200))
    pygame.display.update()
    pygame.time.delay(750)
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    ready = font.render("Set ", True, (0, 0, 0))
    screen.blit(ready, (410, 200))
    pygame.display.update()
    pygame.time.delay(750)
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    ready = font.render("Set. ", True, (0, 0, 0))
    screen.blit(ready, (410, 200))
    pygame.display.update()
    pygame.time.delay(750)
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    ready = font.render("Set.. ", True, (0, 0, 0))
    screen.blit(ready, (410, 200))
    pygame.display.update()
    pygame.time.delay(750)
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    ready = font.render("Set... ", True, (0, 0, 0))
    screen.blit(ready, (410, 200))
    pygame.display.update()
    pygame.time.delay(750)
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    ready = font.render("GO! ", True, (0, 0, 0))
    screen.blit(ready, (410, 200))
    pygame.display.update()
    pygame.time.delay(750)


def help_screen():
    bhelp = True
    while bhelp:
        screen.fill((255, 255, 255))
        screen.blit(helps, (0, 0))
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro()
        pygame.display.update()


def level_select(lvl):
    pygame.time.delay(750)
    bmenu = True
    while bmenu:
        screen.fill((0, 0, 0))
        screen.blit(menu, (0, 0))
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 360 + 220 > mouse[0] > 360 and 80 + 70 > mouse[1] > 80:
            if click[0] == 1:
                lvl = 0
                game(playerX, points_value, playerX_change, milliseconds, seconds, level)
        else:
            screen.blit(lvl1, (360, 80))
        if 360 + 220 > mouse[0] > 360 and 170 + 70 > mouse[1] > 170:
            if click[0] == 1:
                lvl = 1
                game(playerX, points_value, playerX_change, milliseconds, seconds, level)
        else:
            screen.blit(lvl2, (360, 170))
        if 360 + 220 > mouse[0] > 360 and 260 + 70 > mouse[1] > 260:
            if click[0] == 1:
                lvl = 2
                game(playerX, points_value, playerX_change, milliseconds, seconds, level)
        else:
            screen.blit(lvl3, (360, 260))
        pygame.display.update()


# Game Loop
def game(playerX, pts, playerX_change, milliseconds, seconds, lvl):
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    ready()
    for i in range(num_of_each):
        if lvl == 0:
            goodY_change.append(1)
            enemyY_change.append(1)
        if lvl == 1 or lvl == 2:
            goodY_change.append(10)
            enemyY_change.append(10)
    bgame = True
    while bgame:
        # RGB Screen Fill - Red, Green, Blue
        screen.fill((255, 255, 255))

        # setting background
        screen.blit(background, (0, 0))

        # Checking for events (keypress)
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_ESCAPE:
                    level_select(level)

        # changes X position of player character
        playerX += playerX_change

        # Changes y position of enemies and good objects
        for i in range(num_of_each):
            goodY[i] += goodY_change[i]
            enemyY[i] += enemyY_change[i]

            # Checking for collision
            badCollision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
            goodCollision = isCollision(goodX[i], goodY[i], playerX, playerY)

            # Adding points to score
            if goodCollision:
                good_catch = mixer.Sound('good_catch.wav')
                good_catch.play()
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                pts += 100
                print(pts)
                # Sending good object to top of screen in a New location
                goodX[i] = random.randint(0, 862)
                goodY[i] = 0

            if badCollision:
                bad_catch = mixer.Sound('bad_catch.wav')
                # DISPLAY THE SURPRISED FACE HERE FOR 1 SECOND AND REVERT BACK TO NEUTRAL
                bad_catch.play()
                face = random.randint(5, 7)  # HHHHHHHEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                pts -= 50
                print(pts)
                # Sending bad object to top of screen in a new location
                enemyX[i] = random.randint(0, 862)
                enemyY[i] = 0

            if enemyY[i] > 600:
                enemyY[i] = random.randint(0, 200) - 100
            if goodY[i] > 600:
                goodY[i] = random.randint(0, 200) - 100

            enemy(enemyX[i], enemyY[i], i)
            good(goodX[i], goodY[i], i)

        # Setting Boundaries for Recycle Bin --> Doesn't go out of game window
        if playerX <= 0:
            playerX = 0
        elif playerX >= 862:
            playerX = 862

        # Creating Player Object
        player(playerX, playerY)

        # Show Score Function
        show_score(pts, textX, textY)

        # Timer
        if milliseconds > 1000:
            seconds += 1
            milliseconds -= 1000
        if seconds == 60:
            game_over(pts)

        milliseconds += clock.tick_busy_loop(60)

        # Updating display
        pygame.display.update()


intro()
