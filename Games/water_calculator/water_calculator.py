#Water Calculator Game for MC Green robot
#Designed and written by Manas Harbola (harbolam@mcvts.net) on behalf of Middlesex County Academy

import pygame
from PIL import Image

#Define class for water-using appliances
class Appliance:
    def __init__(self, attrDict):
        valid_keys = ['img_src',        #location of image to display
                      'img_resize',     #desired width and length resize image
                      'coordinates',    #coordinates to put image
                      'name',           #name of appliance
                      'sliderQuestion', #question to ask user
                      'units',          #units of use (ex. times, flushes, etc.)
                      'unitRate',       #number of gallons used per unit
                      'usageRange']     #min and max usage in units

        for key in valid_keys:
            setattr(self, key, attrDict.get(key)) #initialize attributes

        self.unitAmt = 0  #current value of units
        self.gallonsUsed = 0 #current amount of water (in gallons) used

    def generate_img(self, screen, img_dims):
        img = Image.open(self.img_src)
        img_resized = img.resize((img_dims[2], img_dims[3]))
        mode = img_resized.mode
        size = img_resized.size
        data = img_resized.tobytes()
        appliance_img = pygame.image.fromstring(data, size, mode).convert_alpha()
        
        screen.blit(appliance_img, (img_dims[0], img_dims[1]))

    def generate_usage(self, surface, x, y, font, color=(0,0,0)):
        TextSurf, TextRect = text_objects(self.name + ': ' + '{0:.0f}'.format(self.gallonsUsed) + ' gallons', font, color)
        TextRect.center = (x, y)
        surface.blit(TextSurf, TextRect)
    
    def menu(self, screen):
        #Button Dimensions
        button_w = 100 / 2; button_h = 125 / 2
        button_x = 0.5 * window_size[0] - 0.5 * button_w
        up_button_y = 0.25 * window_size[1]
        down_button_y = up_button_y + (3 * button_h)

        #Instantiate buttons
        up_button = Button(screen, darker_green, green, (button_x, up_button_y, button_w, button_h), u'\u2191', mediumText)
        down_button = Button(screen, darker_red, red, (button_x, down_button_y, button_w, button_h), u'\u2193', mediumText)
        okay_button = Button(screen, darker_blue, blue, (button_x, 0.75 * window_size[1], 750 / 2, 250 / 2), 'OK', mediumText)
        
        #Portions of the screen that must ONLY be updated (Improves frame rate and performance)
        setting_rect = pygame.rect.Rect(button_x, up_button_y, 512 / 2, 4 * up_button_y) #Portion of screen which adjusts value
        back_rect = pygame.rect.Rect(button_x, 0.75 * window_size[1], 750 / 2, 250 / 2) #Portion of screen for the back button
        
        updateList = [setting_rect, back_rect]

        #Prepare title text and location
        QuestionSurf, QuestionRect = text_objects(self.sliderQuestion, largeText, white)
        QuestionRect.center = ((window_size[0] / 2), (window_size[1] / 8))

        #Make entire screen white to 'clean' it
        screen.fill(white)
        
        #Write background image to buffer
        screen.blit(background, backgroundRect)

        #Write text and image to buffer
        screen.blit(QuestionSurf, QuestionRect)
        self.generate_img(screen, self.coordinates + self.img_resize)

        #Update ENTIRE screen just once
        pygame.display.update()

        #Store as previous value of unit rectangle
        UnitRect = pygame.rect.Rect(0,0,0,0)

        running = True

        while running:
            #Handle events here:
            for event in pygame.event.get():
                print(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_status = True

                    #Check if buttons are pressed if mouse button is down
                    if up_button.is_pressed(touch_status):
                        if self.unitAmt < self.usageRange[1]:
                            self.unitAmt += 1
                            self.gallonsUsed = self.unitAmt * self.unitRate

                    if down_button.is_pressed(touch_status):
                        if self.unitAmt > self.usageRange[0]:
                            self.unitAmt -= 1
                            self.gallonsUsed = self.unitAmt * self.unitRate

                    if okay_button.is_pressed(touch_status):
                        game_menu(gameDisplay)

                else:
                    touch_status = False

            #Used for going from text with n digit unitAmt to n - 1 digit unitAmt
            #screen.fill(white, UnitRect)
            screen.blit(background, dest=UnitRect, area=UnitRect)

            #Prepare to display current unitAmt between buttons
            UnitSurf, UnitRect = text_objects(str(self.unitAmt) + ' ' + self.units, mediumText, white)
            UnitRect.topleft = (button_x, up_button_y + 1.5 * button_h)
    
            #Fill the area where the unitAmt text goes with white to 'refresh' it
            #screen.fill(white, UnitRect)
            #screen.blit(background, dest=UnitRect, area=UnitRect)
            screen.blit(UnitSurf, UnitRect)

            up_button.generate()
            down_button.generate()
            okay_button.generate()

            pygame.display.update(updateList)
            clock.tick(FPS)

#Render text to a surface and a corresponding rectangle
def text_objects(text, font, color=(0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


#Class for generating buttons
class Button:
    def __init__ (self, surfaceName, ac, ic, rectVals, text, font):
        self.ac = ac #Active color of button
        self.ic = ic #Inactive color of button
        self.rectAttrs = rectVals #(x, y, w, h) of button
        self.surfaceName = surfaceName
        self.text = text
        self.font = font

    def generate(self):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()

        #Check if mouse is on button
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.surfaceName, self.ac, self.rectAttrs)

        #Else just show darker button
        else:
            pygame.draw.rect(self.surfaceName, self.ic, self.rectAttrs)

        textSurf, textRect = text_objects(self.text, self.font)

        textRect.center = (x + (w / 2), y + (h / 2))
        self.surfaceName.blit(textSurf, textRect)

    def get_rect(self):
        x, y, w, h = self.rectAttrs
        return pygame.rect.Rect(x, y, w, h)

    def is_pressed(self, touch_status):
        x, y, w, h = self.rectAttrs
        mouse = pygame.mouse.get_pos()
        
        #Check if mouse is hovering over button or not
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if touch_status == True:
                #print('CLICK DETECTED')
                return True

            elif touch_status == False:
                return False

        #If mouse is not hovering over button, button must obviously not be pressed
        else:
            return False

#Initiate pygame
pygame.init() #SUPER IMPORTANT

#Screen size of window
window_size = (1920,1080)

#Max FPS (frames per second) of game
FPS = 30

#Define basic colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
darker_red = (200, 0, 0)
green = (0, 255, 0)
darker_green = (0, 200, 0)
blue = (50, 89, 250)
darker_blue = (35, 67, 250)

#Define basic text sizes
largeText = pygame.font.Font('FreeSansBold.ttf', 64)   #Large text, ideal for headings
mediumText = pygame.font.Font('FreeSansBold.ttf', 48)   #Medium text, ideal for subheadings
mediumText2 = pygame.font.Font('FreeSansBold.ttf', 24)
smallText =  pygame.font.Font('FreeSansBold.ttf', 16)   #Small text, ideal for small buttons


#Define background
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, window_size)
backgroundRect = background.get_rect()

#Instantiate window/surface
gameDisplay = pygame.display.set_mode(window_size)
pygame.display.set_caption('Water Calculator')
clock = pygame.time.Clock()

#ok
dishwasher_info = {'img_src': 'dishwasher.png', 'img_resize': (256,256), 'coordinates': (window_size[0] / 4, window_size[1] / 4), 
                   'name': 'Dishwasher', 'sliderQuestion': 'How Often Do You Use The Dishwasher in a Week?',
                   'units': 'times', 'unitRate': 6, 'usageRange':(0, 10)}
#ok
washing_machine_info = {'img_src': 'washing_machine.png', 'img_resize': (300,400), 'coordinates': (window_size[0] / 4, window_size[1] / 4), 
                   'name': 'Washing Machine', 'sliderQuestion': 'How Often Do You Use The Washing Machine in a Week?',
                   'units': 'times', 'unitRate': 40, 'usageRange':(0, 10)}
#ok
shower_info = {'img_src': 'shower.png', 'img_resize': (512 // 2,512 // 2), 'coordinates': (window_size[0] / 4, window_size[1] / 4), 
                   'name': 'Shower', 'sliderQuestion': 'How Often Do You Use The Shower in a Week?',
                   'units': 'times', 'unitRate': 17.2, 'usageRange':(0, 20)}
#ok
toilet_info = {'img_src': 'toilet.png', 'img_resize': (312 // 2,512  // 2), 'coordinates': (window_size[0] / 4, window_size[1] / 4), 
                   'name': 'Toilet', 'sliderQuestion': 'How Often Do You Use The Toilet in a Week?',
                   'units': 'times', 'unitRate': 1.6, 'usageRange':(0, 30)}

sink_info = {'img_src': 'sink.png', 'img_resize': (728 // 2 ,512 // 2), 'coordinates': (window_size[0] / 4, window_size[1] / 4), 
                   'name': 'Sink', 'sliderQuestion': 'How Many Hours Do You Use The Kitchen Sink in a Week?',
                   'units': 'hours', 'unitRate': 2.2*60, 'usageRange':(0, 168)}
#ok
faucet_info = {'img_src': 'faucet.png', 'img_resize': (333 // 2 ,512 // 2), 'coordinates': (window_size[0] / 4, window_size[1] / 4), 
                   'name': 'Faucet', 'sliderQuestion': 'How Many Hours Do You Use The Faucet in a Week?',
                   'units': 'hours', 'unitRate': 1.5*60, 'usageRange':(0, 168)}

#Instantiate appliance objects
dishwasher = Appliance(dishwasher_info)
washing_machine = Appliance(washing_machine_info)
shower = Appliance(shower_info)
toilet = Appliance(toilet_info)
sink = Appliance(sink_info)
faucet = Appliance(faucet_info)

#Start Menu for Game
def game_intro(surface):
    #Button Dimensions
    button_w = 750 / 2; button_h = 250 / 2
    help_button_x = 270; button_y = 1300 / 2
    button_spacing = 237 / 2   #spacing between buttons in px
    play_button_x = help_button_x + button_w + button_spacing
    quit_button_x = play_button_x + button_w + button_spacing
    
    #Instantiate buttons (Only needs to be done once)
    help_button = Button(surface, blue, darker_blue, (help_button_x, button_y, button_w, button_h), 'Help', mediumText)
    play_button = Button(surface, green, darker_green, (play_button_x, button_y, button_w, button_h), 'Play', mediumText)
    quit_button = Button(surface, red, darker_red, (quit_button_x, button_y, button_w, button_h), 'Quit', mediumText)
    
    #Portion of the screen that must ONLY be updated
    help_button_rect = help_button.get_rect()
    play_button_rect = play_button.get_rect()
    quit_button_rect = quit_button.get_rect()
    updateList = [help_button_rect, play_button_rect, quit_button_rect]

    #Prepare title text and location
    TextSurf, TextRect = text_objects('How Much Water Do You Use At Home?', largeText, white)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 4))

    #Make entire screen white to 'clean' the screen
    surface.fill(white)

    #Write background image to buffer
    surface.blit(background, backgroundRect)

    #Write text to buffer
    surface.blit(TextSurf, TextRect)

    #Update ENTIRE screen just once
    pygame.display.update()

    touch_status = False #False = no touch, True = touch present

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print('Pressed')
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if quit_button.is_pressed(touch_status):    #If 'Quit' button is tapped
                    pygame.quit()
                    quit()

                if play_button.is_pressed(touch_status):    #If 'Play' button is tapped
                    game_menu(gameDisplay)

                if help_button.is_pressed(touch_status):    #If 'Help' button is tapped
                    game_help(gameDisplay)
            else:
                touch_status = False

        help_button.generate()
        play_button.generate()
        quit_button.generate()

        #Update only the portions that need to be updated
        pygame.display.update(updateList)
        clock.tick(FPS)


#Help Menu for Game
def game_help(surface):
    #Instantiate button for returning back to intro page
    back_button = Button(surface, darker_green, green, (0.5 * window_size[0] - 150 , 0.75 * window_size[1], 750 / 2, 250 / 2), 'Back', mediumText)

    #back_button_rect = pygame.rect.Rect(back_button.rectAttrs[0], back_button.rectAttrs[1], back_button.rectAttrs[2], back_button.rectAttrs[3])
    back_button_rect = back_button.get_rect()
    updateList = [back_button_rect]
    
    TextSurf, TextRect = text_objects('How to Play:', largeText, white)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 4))
    
    line_spacing = 75   #Spacing between each line of instructions

    Line1Surf, Line1Rect = text_objects('1.) Select a button under an appliance to set its value', mediumText, white)
    Line1Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + 150)
    
    Line2Surf, Line2Rect = text_objects('2.) After you are done, tap the \'Back\' button to return to the main screen', mediumText, white)
    Line2Rect.center = ((window_size[0] / 2), (window_size[1] / 4) + 150 + (2 * line_spacing))

    #Make entire screen white to clean it
    surface.fill(white)
    
    #Write background image to buffer
    surface.blit(background, backgroundRect)

    #Write text to buffer
    surface.blit(TextSurf, TextRect)
    surface.blit(Line1Surf, Line1Rect)
    surface.blit(Line2Surf, Line2Rect)

    #Update ENTIRE screen just once
    pygame.display.update()

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #print('Pressed')
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if back_button.is_pressed(touch_status):
                    #print('Intro Activated')
                    game_intro(gameDisplay)
            else:
                touch_status = False

        surface.fill(white)
        back_button.generate()

        pygame.display.update(updateList)
        clock.tick(FPS)

#Provide tips on how to reduce water usage
def game_tips(surface):
    #Instantiate button for returning back to intro page
    back_button = Button(surface, darker_green, green, (0.5 * window_size[0] - 150 , 0.80 * window_size[1], 750 / 2, 250 / 2), 'Back', mediumText)

    #back_button_rect = pygame.rect.Rect(back_button.rectAttrs[0], back_button.rectAttrs[1], back_button.rectAttrs[2], back_button.rectAttrs[3])
    back_button_rect = back_button.get_rect()
    updateList = [back_button_rect]
    
    #Make entire screen white to clean it
    surface.fill(white)
    
    #Write background image to buffer
    surface.blit(background, backgroundRect)

    TextSurf, TextRect = text_objects('Ways to reduce your water consumption:', largeText, white)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 4))
    surface.blit(TextSurf, TextRect)

    line_spacing = 50   #Spacing between each line of instructions
    
    #set limits for each appliance usage
    limits = [dishwasher.unitAmt > 7, washing_machine.unitAmt > 3, shower.unitAmt > 14,
              toilet.unitAmt > 14, sink.unitAmt > 10, faucet.unitAmt > 10]
    advice = ['Use the dishwasher less often, settle for washing with your hands',
              'Use the washing machine less often, or invest in a water-efficient one',
              'Try investing in a water-efficient shower head', 
              'Try investing in a water-efficient toilet',
              'Turn off the sink when you finish using it',
              'Turn off the faucet when you finish using it']
    

    x, y = window_size[0] / 2, (window_size[1] / 4) + 150
    count = 1

    for i in range(len(limits)):
        flag = limits[i]
        if flag:
            LineSurf, LineRect = text_objects(str(count) + '.) ' + advice[i], mediumText, white)
            LineRect.center = (x, y)
            surface.blit(LineSurf, LineRect)
            y += 1.5 * line_spacing
            count += 1
            
    #Update ENTIRE screen just once
    pygame.display.update()

    running = True

    while running:

        #Handle events here:
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if back_button.is_pressed(touch_status):
                    game_menu(surface)
            else:
                touch_status = False

        back_button.generate()

        pygame.display.update(updateList)
        clock.tick(FPS)



#Main menu for game
def game_menu(surface):
    #Define appliance button dimensions
    button_w = 325 / 2; button_h = 125 / 2

    #row spacing is distance between the top left corners of two horizontally distant buttons
    row_spacing = button_w + 150
    
    #same as row spacing but for column
    column_spacing = button_h + 300
    
    #x and y values of top left button
    ref_x = 0.125 * window_size[0]; ref_y = 0.45 * window_size[1]

    #Top Row
    dish_dims =   (ref_x, ref_y, button_w, button_h)
    wash_dims =   (ref_x + row_spacing, ref_y, button_w, button_h)
    shower_dims = (ref_x + 2 * row_spacing, ref_y, button_w, button_h)
    
    #Bottom Row
    toilet_dims = (ref_x, ref_y + column_spacing, button_w, button_h)
    sink_dims =   (ref_x + row_spacing, ref_y + column_spacing, button_w, button_h)
    faucet_dims = (ref_x + 2 * row_spacing, ref_y + column_spacing, button_w, button_h)
    
    #Back/Tips/Quit button dimensions
    back_dims = (0.575 * window_size[0], 0.75 * window_size[1], button_w, button_h)
    tips_dims = (0.575 * window_size[0] + (row_spacing - 60), 0.75 * window_size[1], button_w, button_h)
    quit_dims = (0.575 * window_size[0] + 2.0 * (row_spacing - 60), 0.75 * window_size[1], button_w, button_h)
    
    #INSTANTIATE BUTTONS HERE
    dish_button =   Button(surface, green, darker_green, dish_dims, dishwasher.name, smallText)
    wash_button =   Button(surface, green, darker_green, wash_dims, washing_machine.name, smallText)
    shower_button = Button(surface, green, darker_green, shower_dims, shower.name, smallText)
    toilet_button = Button(surface, green, darker_green, toilet_dims, toilet.name, smallText)
    sink_button =   Button(surface, green, darker_green, sink_dims, sink.name, smallText)
    faucet_button = Button(surface, green, darker_green, faucet_dims, faucet.name, smallText)
    back_button =   Button(surface, blue, darker_blue, back_dims, 'Back', mediumText)
    quit_button =   Button(surface, red, darker_red, quit_dims, 'Quit', mediumText)
    tips_button =   Button(surface, green, darker_green, tips_dims, 'Tips', mediumText)

    #Instantiate areas to update
    dish_rect = dish_button.get_rect()
    wash_rect = wash_button.get_rect()
    shower_rect = shower_button.get_rect()
    toilet_rect = toilet_button.get_rect()
    sink_rect = sink_button.get_rect()
    faucet_rect = faucet_button.get_rect()
    back_rect = back_button.get_rect()
    quit_rect = quit_button.get_rect()
    tips_rect = tips_button.get_rect()

    updateList = [dish_rect, wash_rect, shower_rect, toilet_rect,
                  sink_rect, faucet_rect, back_rect, quit_rect, tips_rect]
    

    #Prepare titles, text and locations
    TextSurf, TextRect = text_objects('How Much Water Do You Use At Home?', largeText, white)
    TextRect.center = ((window_size[0] / 2), (window_size[1] / 8))
    
    #Prepare subheading
    TotalSurf, TotalRect = text_objects('Total Water Usage:', mediumText, white)
    TotalRect.center = ((0.75 * window_size[0]), (window_size[1] / 4))

    #Prepare title for total
    gallon_sum = dishwasher.gallonsUsed + washing_machine.gallonsUsed + shower.gallonsUsed + toilet.gallonsUsed + sink.gallonsUsed + faucet.gallonsUsed

    #SumSurf, SumRect = text_objects('Total: ' + str(gallon_sum) + ' gallons per day', mediumText, white)
    SumSurf, SumRect = text_objects('Total: ' + '{0:.0f}'.format(gallon_sum) + ' gallons per week', mediumText, white)

    SumRect.center = ((0.75 * window_size[0]), (window_size[1] / 4 + 450))

    #Make entire screen white to 'clean' it
    surface.fill(white)

    #Write background image to buffer
    surface.blit(background, backgroundRect)

    #Write text to buffer
    surface.blit(TextSurf, TextRect)
    surface.blit(TotalSurf, TotalRect)
    surface.blit(SumSurf, SumRect)

    #Write water usage for each item to buffer
    dishwasher.generate_usage(surface, (0.75 * window_size[0]), (window_size[1] / 4 + 100), mediumText2, white)
    washing_machine.generate_usage(surface, (0.75 * window_size[0]), (window_size[1] / 4 + 150), mediumText2, white)
    shower.generate_usage(surface, (0.75 * window_size[0]), (window_size[1] / 4 + 200), mediumText2, white)
    toilet.generate_usage(surface, (0.75 * window_size[0]), (window_size[1] / 4 + 250), mediumText2, white)
    sink.generate_usage(surface, (0.75 * window_size[0]), (window_size[1] / 4 + 300), mediumText2, white)
    faucet.generate_usage(surface, (0.75 * window_size[0]), (window_size[1] / 4 + 350), mediumText2, white)


    #Write images to buffer
    dishwasher.generate_img(surface, (ref_x - 20, ref_y - 225, 200, 200))
    washing_machine.generate_img(surface, (ref_x + row_spacing + 5, ref_y - 225, 150, 200))
    shower.generate_img(surface, (ref_x + 2 * row_spacing + 20, ref_y - 225, 200, 200))
    
    toilet.generate_img(surface, (ref_x + 20, ref_y + column_spacing - 225, 120, 200))
    sink.generate_img(surface, (ref_x + row_spacing - 30, ref_y + column_spacing - 225, 280, 200))
    faucet.generate_img(surface, (ref_x + 2 * row_spacing + 20, ref_y + column_spacing - 225, 120, 200))

    #Refresh ENTIRE screen ONCE
    pygame.display.update()
    
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_status = True

                #Check if buttons are pressed if mouse button is down
                if dish_button.is_pressed(touch_status):
                    dishwasher.menu(surface)
                if wash_button.is_pressed(touch_status):
                    washing_machine.menu(surface)
                if shower_button.is_pressed(touch_status):
                    shower.menu(surface)
                if toilet_button.is_pressed(touch_status):
                    toilet.menu(surface)
                if sink_button.is_pressed(touch_status):
                    sink.menu(surface)
                if faucet_button.is_pressed(touch_status):
                    faucet.menu(surface)
                if back_button.is_pressed(touch_status):
                    game_intro(surface)
                if tips_button.is_pressed(touch_status):
                    game_tips(surface)
                if quit_button.is_pressed(touch_status):
                    pygame.quit()
                    quit()
    
        dish_button.generate()
        wash_button.generate()
        shower_button.generate()
        toilet_button.generate()
        sink_button.generate()
        faucet_button.generate()
        back_button.generate()
        quit_button.generate()
        tips_button.generate()

        pygame.display.update(updateList)

#Execute game
game_intro(gameDisplay)

pygame.quit()
quit()
