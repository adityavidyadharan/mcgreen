import pygame
from pygame import mixer
import time
import sys
sys.path.append("../")
from head_controller import Head_comm

controller = Head_comm("What's Wrong with the Room")

pygame.init()
screen = pygame.display.set_mode((926, 634))

# backgrounds
classroomlvl = pygame.image.load('classroomlvl.png')
kitchenlvl = pygame.image.load('kitchenlvl.png')
bedroomlvl = pygame.image.load('bedroomlvl.png')
menu = pygame.image.load('menubkg.png')
helps = pygame.image.load('helpbkg.png')
gamewon = pygame.image.load('winner.png')
gamelost = pygame.image.load('loser.png')

# Background Music
mixer.music.load('backgroundmsc.wav')

# kitchen level items
can = pygame.image.load('can.png')
looseplant = pygame.image.load('loose_plant.png')
papertowel = pygame.image.load('paper_towel.png')
pottedplant = pygame.image.load('potted_plant.png')
recyclingarrow = pygame.image.load('recycling_arrow.png')
runningfaucet = pygame.image.load('running_faucet.png')
towels = pygame.image.load('towels.png')
tick = pygame.image.load('tick.png')

# Buttons
playb = pygame.image.load('playbtn.png')
helpb = pygame.image.load('helpbtn.png')
exitb = pygame.image.load('quitbtn.png')
lvl1 = pygame.image.load('lvl1.png')
lvl2 = pygame.image.load('lvl2.png')
lvl3 = pygame.image.load('lvl3.png')
hintp = pygame.image.load('hint.png')
blank = pygame.image.load('blank.png')

# classroom level items
closedcurtains = pygame.image.load('cosed_curtains.png')
opencurtains = pygame.image.load('open_curtains.png')
trash = pygame.image.load('trash.png')
compost = pygame.image.load('compost.png')
laptopoff = pygame.image.load('laptop_off.png')
laptopon = pygame.image.load('laptop_on.png')
papertrash = pygame.image.load('paper_trash.png')
paperrecycling = pygame.image.load('paper_recycling.png')

# bedroom level items
openwindow = pygame.image.load('open_window.png')
closedwindow = pygame.image.load('closed_window.png')
loosepaper = pygame.image.load('loose_paper.png')
whiteboard = pygame.image.load('whiteboard.png')
waterbottle = pygame.image.load('waterbottle.png')
reusablewb = pygame.image.load('reusable_water_bottle.png')
ipad = pygame.image.load('ipad.png')
lighton = pygame.image.load('light_on.png')
lightoff = pygame.image.load('light_off.png')

pygame.display.set_caption("What's Wrong With The Room?")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

font = pygame.font.Font('Bubblegum.ttf', 32)

clock = pygame.time.Clock()

start_time = pygame.time.get_ticks()


def intro():
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    controller.face_update(4)  # HHHHHHHHHHHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRRRRREEEEEEEEEEEEEE
    bmenu = True
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
                level_select()
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


def help_screen():
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
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


def level_select():
    pygame.time.delay(750)
    bmenu = True
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    while bmenu:
        screen.fill((255, 255, 255))
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
                level1()
        else:
            screen.blit(lvl1, (360, 80))
        if 360 + 220 > mouse[0] > 360 and 170 + 70 > mouse[1] > 170:
            if click[0] == 1:
                level2()
        else:
            screen.blit(lvl2, (360, 170))
        if 360 + 220 > mouse[0] > 360 and 260 + 70 > mouse[1] > 260:
            if click[0] == 1:
                level3()
        else:
            screen.blit(lvl3, (360, 260))
        pygame.display.update()


def gamewin():
    face = random.randint(1, 3)  # HEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRREEEEEEEEEEEEEE
    controller.face_update(face)
    # These commands won't over write themselves right? like if i say these three in a row
    # it'll hit all of the positions before going back to [90,90]?
    controller.head_update([90, 45])
    controller.head_update([90, 135])
    controller.head_update([90, 90])
    bgame = True
    mixer.music.load('game_won.wav')
    mixer.music.play()
    while bgame:
        screen.fill((255, 255, 255))
        screen.blit(gamewon, (0,0))
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level_select()
        pygame.display.update()


def gamelose():
    face = random.randint(5, 7)  # HHHHHHHHHHHHHHEEEEEEEEEEEEERRRRRRRRRRRREEEEEEEEEEEE
    controller.face_update(face)
    # See game_won head update comments
    controller.head_update([45, 90])
    controller.head_update([135, 90])
    controller.head_update([90, 90])
    bgame = True
    mixer.music.load('game_lose.wav')
    mixer.music.play()
    while bgame:
        screen.fill((255, 255, 255))
        screen.blit(gamelost, (0, 0))
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level_select()
        pygame.display.update()


def level1():
    obj1 = True
    obj2 = True
    obj3 = True
    obj4 = True
    lvl1 = True
    hint = font.render(" ", True, (0, 0, 0))
    obj1pic = closedcurtains
    obj2pic = papertrash
    obj3pic = trash
    obj4pic = laptopon
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    while lvl1:
        screen.blit(classroomlvl, (0, 0))
        screen.blit(hint, (50, 25))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(mouse)
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level_select()
        if 850 > mouse[0] > 750 and 220 > mouse[1] > 90:
            screen.blit(obj1pic, (750, 90))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj1pic = opencurtains
                obj1 = False
        else:
            screen.blit(obj1pic, (750, 90))
        if 380 > mouse[0] > 280 and 360 > mouse[1] > 210:
            screen.blit(obj2pic, (280, 230))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj2pic = paperrecycling
                obj2 = False
        else:
            screen.blit(obj2pic, (280, 230))
        if 165 > mouse[0] > 58 and 410 > mouse[1] > 265:
            screen.blit(obj3pic, (58, 265))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj3pic = compost
                obj3 = False
        else:
            screen.blit(obj3pic, (58, 265))
        if 550 > mouse[0] > 440 and 380 > mouse[1] > 315:
            screen.blit(obj4pic, (440, 315))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj4pic = laptopoff
                obj4 = False
        else:
            screen.blit(obj4pic, (440, 315))
        if 900 > mouse[0] > 815 and 100 > mouse[1] > 25:
            screen.blit(hintp, (815, 25))
            if click[0] == 1:
                if obj1:
                    hint = font.render("Hint: Always try to use Natural Sunlight", True, (0, 0, 0))
                elif obj2:
                    hint = font.render("Hint: Always Recycle Paper", True, (0, 0, 0))
                elif obj3:
                    hint = font.render("Hint: Turn food waste into Compost", True, (0, 0, 0))
                elif obj4:
                    hint = font.render("Hint: Turn off things you aren't using", True, (0, 0, 0))
        else:
            screen.blit(hintp, (815, 25))
        if obj1 is False and obj2 is False and obj3 is False and obj4 is False:
            gamewin()
        pygame.display.update()


def level2():
    obj1 = True
    obj2 = True
    obj3 = True
    obj4 = True
    obj5 = True
    lvl2 = True
    hint = font.render(" ", True, (0, 0, 0))
    obj1pic = blank
    obj2pic = loosepaper
    obj3pic = waterbottle
    obj4pic = openwindow
    obj5pic = lighton
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    while lvl2:
        screen.blit(bedroomlvl, (0, 0))
        screen.blit(hint, (50, 25))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(mouse)
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level_select()
        if 605 > mouse[0] > 550 and 425 > mouse[1] > 390:
            screen.blit(obj1pic, (540, 370))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj1pic = ipad
                obj1 = False
        else:
            screen.blit(obj1pic, (540, 370))
        if 320 > mouse[0] > 240 and 410 > mouse[1] > 365:
            screen.blit(obj2pic, (240, 365))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj2pic = whiteboard
                obj2 = False
        else:
            screen.blit(obj2pic, (240, 365))
        if 60 > mouse[0] > 20 and 500 > mouse[1] > 420:
            screen.blit(obj3pic, (20, 420))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj3pic = reusablewb
                obj3 = False
        else:
            screen.blit(obj3pic, (20, 420))
        if 820 > mouse[0] > 650 and 290 > mouse[1] > 120:
            screen.blit(obj4pic, (650, 120))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj4pic = closedwindow
                obj4 = False
        else:
            screen.blit(obj4pic, (650, 120))
        if 345 > mouse[0] > 280 and 290 > mouse[1] > 230:
            screen.blit(obj5pic, (290, 240))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj5pic = lightoff
                obj5 = False
        else:
            screen.blit(obj5pic, (290, 240))
        if 900 > mouse[0] > 815 and 100 > mouse[1] > 25:
            screen.blit(hintp, (815, 25))
            if click[0] == 1:
                if obj1:
                    hint = font.render("Hint: Turn off things you aren't using", True, (0, 0, 0))
                elif obj2:
                    hint = font.render("Hint: Recycle Paper as much as Possible", True, (0, 0, 0))
                elif obj3:
                    hint = font.render("Hint: Use Very Little Plastic (Bottles, Bags, etc.) ", True, (0, 0, 0))
                elif obj4:
                    hint = font.render("Hint: Close Windows to Keep Your House Warm/Cold", True, (0, 0, 0))
                elif obj5:
                    hint = font.render("Hint: Turn off things you aren't using", True, (0, 0, 0))
        else:
            screen.blit(hintp, (815, 25))

        if obj1 is False and obj2 is False and obj3 is False and obj4 is False and obj5 is False:
            gamewin()
        pygame.display.update()


def level3():
    obj1 = True
    obj2 = True
    obj3 = True
    obj4 = True
    obj5 = True
    lvl3 = True
    hint = font.render(" ", True, (0, 0, 0))
    obj1pic = papertowel
    obj2pic = papertowel
    obj3pic = can
    obj4pic = runningfaucet
    obj5pic = blank
    passed_time = pygame.time.get_ticks() - start_time
    milliseconds = 0
    seconds = -round(passed_time/1000)
    mixer.music.load('backgroundmsc.wav')
    mixer.music.play(-1)
    while lvl3:
        screen.blit(kitchenlvl, (0, 0))
        screen.blit(hint, (50, 25))
        screen.blit(papertowel, (550, 540))
        time = font.render(str(seconds), True, (0, 0, 0))
        screen.blit(time, (25, 50))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(mouse)
        for event in pygame.event.get():
            # Quitting the Game by X-ing out Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keystroke check (right/left) and changing val of playerX_change to +/- based on keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level_select()
        if 625 > mouse[0] > 550 and 605 > mouse[1] > 540:
            screen.blit(obj1pic, (550, 540))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj1pic = recyclingarrow
                obj1 = False
        else:
            screen.blit(obj1pic, (550, 540))
        if 450 > mouse[0] > 350 and 380 > mouse[1] > 300:
            screen.blit(obj2pic, (375, 325))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj2pic = towels
                obj2 = False
        else:
            screen.blit(obj2pic, (375, 325))
        if 680 > mouse[0] > 640 and 370 > mouse[1] > 335:
            screen.blit(obj3pic, (640, 305))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj3pic = pottedplant
                obj3 = False
        else:
            screen.blit(obj3pic, (640, 305))
        if 340 > mouse[0] > 265 and 355 > mouse[1] > 300:
            screen.blit(obj4pic, (265, 300))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj4pic = blank
                obj4 = False
        else:
            screen.blit(obj4pic, (265, 300))
        if 160 > mouse[0] > 5 and 535 > mouse[1] > 345:
            screen.blit(obj5pic, (5, 345))
            if click[0] == 1:
                face = random.randint(1, 3)  # HHHHHEEEEEEEEEEEEEEERRRRRRRRRRRRREEEEEEEEEEEEE
                controller.face_update(face)
                # should i delay here? cuz it's gonna delay the entire program or is that on ur end?
                # either way i'll include and u can play around
                # time.sleep(2)
                controller.face_update(4)
                obj5pic = tick
                obj5 = False
        else:
            screen.blit(obj5pic, (5, 345))
        if 900 > mouse[0] > 815 and 100 > mouse[1] > 25:
            screen.blit(hintp, (815, 25))
            if click[0] == 1:
                if obj1:
                    hint = font.render("Hint: Use Things made from Recycled Materials", True, (0, 0, 0))
                elif obj2:
                    hint = font.render("Hint: Avoid Using Paper as much as you can", True, (0, 0, 0))
                elif obj3:
                    hint = font.render("Hint: Create your own projects with recyclables ", True, (0, 0, 0))
                elif obj4:
                    hint = font.render("Hint: Don't leave the water running", True, (0, 0, 0))
                elif obj5:
                    hint = font.render("Hint: Turn off/Close things you aren't using", True, (0, 0, 0))
        else:
            screen.blit(hintp, (815, 25))

        if obj1 is False and obj2 is False and obj3 is False and obj4 is False and obj5 is False:
            gamewin()

        if milliseconds > 1000:
            seconds -= 1
            milliseconds -= 1000
        if seconds < 0:
            seconds = 92
        if seconds == 0:
            if obj1 is False and obj2 is False and obj3 is False and obj4 is False and obj5 is False:
                gamewin()
            else:
                gamelose()

        milliseconds += clock.tick_busy_loop(60)
        pygame.display.update()


intro()