import pygame
import sys
sys.path.append('arcade_resources')
import spritesheet
from pygame._sdl2.video import Window
from snake import*
from SpacePong import SpacePong_play
from flappyboom import*

# initializations from the pygame module #/
pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()

# window = Window.from_display_module()
# window.position = (300, 200)/

# - - - - - - window settings - - - - - - - #
# window constants #
WIN_WIDTH, WIN_HEIGHT = 1120, 630

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
title = 'Arcade Games'
pygame.display.set_caption(title)

# - - - - - - Loading Images - - - - - - #

# character spritesheet 

'''I created a python module called 'spritesheet' where in the class spritesheet extracts
the individual frames from a spritesheet, and stores them into a list without having to
call in each individual frame of the player animation'''

sprite_sheet_image = pygame.image.load('arcade_resources/playerboom.png').convert_alpha()   
PINK = (255, 174, 201)                                                          #color key
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)                      #initializing image as self in class SpriteSheet

''' 
Animation list is the nested master list of all frames of the spritesheet per action
this includes: idle frames, walking left and right frames, and the playing frames

While animation steps is a list of how many frames there are per each action
so idle has 6 frames, walk right and walk left have 8 frames, and the playing action has 3 frames'''

animation_steps = [6,8,8,3]
animation_list = []                                                            
step_counter = 0                                                                  #step couteer is used for the extraction of each frame from the spritesheet 
for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 20, 39, 7, PINK))
        step_counter += 1
    animation_list.append(temp_img_list)

# background_image 
background = pygame.transform.scale(pygame.image.load('arcade_resources/background.png'), (1120, 630))
background2 = pygame.transform.scale(pygame.image.load('arcade_resources/arcadelightson.png'), (1120, 630))
background_anim =[background,background2]

# blink animation 
blink = pygame.transform.scale(pygame.image.load('arcade_resources/screenblink.png'), (10*7,10*7))

# - - - - - Animation Timer Initialization - - - - - #
'''called as global variables because they will be used in Player Class'''
now_time = 0
last_update_bg = 0
frame_bg = 0
### ======================= MAIN FUNCTION =========================== ##
''' A function containing all necessary code for the overworld '''

def main():

    pygame.display.set_mode((1120, 630))
    
    # variables #
    FPS = 24
    clock = pygame.time.Clock()

    #creating a player object
    class Player(object):     
        global keys
        def __init__(self, width, height):
            self.x = 11*7                                             # the x coordinates of player (spawn point is 11*7)
            self.y = 38*7                                             # the y coordinate of player
            self.width = width
            self.height = height
            self.vel = 10                                             # velocity of player, will be used to move player left and right
            self.left = False                                       
            ''' initial boolean values for character movement animation '''
            self.standing_pos = 0
            self.right = False
            self.backidle = False
            self.walkCount = 0
            self.backCount = 0
            self.num = 0                                              # will be used for blinking animation of the screens in arcade

        # a function for the player animation movement #
        def movement(self):
            '''if left, right, space are pressed then this changes the bool values used for character animation
            determines what to animate. Also changes the x values by the set velocity to change the coordinates of player'''
            
            # left key for left movement + the conditions for screen boundaries 
            if keys[pygame.K_LEFT] and self.x > self.vel and self.x > 4*7:
                self.x -= self.vel
                self.left = True
                self.right = False
                self.backidle = False
                self.num = 0
            
            # right key for right movement + the conditions for screen boundaries 
            elif keys[pygame.K_RIGHT] and self.x < 135*7:
                self.x += self.vel
                self.right = True
                self.left = False
                self.backidle = False
                self.num = 0

            # The next 5 conditions are for the playing animation or the back idle animation : x coordinate is compared to the coordinates of arcades
            elif 38*7 <= self.x < 53*7 and self.x+11*7 < 53*7 and keys[pygame.K_e]:
                self.backidle = True
                self.num = 1
      
            elif 60*7 <= self.x < 75*7 and self.x+11*7 < 75*7 and keys[pygame.K_e]:
                self.backidle = True
                self.num = 2

            elif 82*7 <= self.x < 97*7 and self.x+11*7 <97*7 and keys[pygame.K_e]:
                self.backidle = True
                self.num = 3

            elif 104*7 <= self.x < 119*7 and self.x+11*7 < 119*7 and keys[pygame.K_e]:
                self.backidle = True
                self.num = 4

            elif 126*7 <= self.x < 141*7 and self.x+11*7 < 144*7 and keys[pygame.K_e]:
                self.backidle = True
                self.num = 5

            # returns bools left and right to false to return to standing idle animation
            else:
                self.left = False
                self.right = False

            #returns value of num = which will be used for the blinking animation of the arcades
            return self.num
            
        def draw(self, win):
            '''draws and blits the character onto the window screen based on the bool values from
            the movement function '''

            global now_time             #will be used for animation timer ticks
   
            if self.walkCount + 1 > 24: #24 is the fps the walking sprite frames depend on walkcount variable
                self.walkCount = 0
            
            if self.backCount + 1 == 3: #for the back idle animation which only contains 3 frames
                self.backCount = 0

            if self.left:               #if left then the player object will be blitted towards the left
                win.blit(animation_list[2][self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            elif self.right:            #if right then the player object will be blitted towards the left
                win.blit(animation_list[1][self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            
            elif self.backidle:         #if backidle then the player object will be blitted onto the arcade machines
                if time - now_time >= 250:
                    self.backCount += 1
                    now_time = pygame.time.get_ticks()
                win.blit(animation_list[3][self.backCount], (self.x, self.y))

            else:                            #else return to idle animation
                if time - now_time >= 750:   # timer
                    self.standing_pos += 1
                    now_time = pygame.time.get_ticks()  
                if self.standing_pos % 6 == 0:
                    self.standing_pos = 0
                    win.blit(animation_list[0][self.standing_pos], (self.x, self.y))
                else:
                    win.blit(animation_list[0][self.standing_pos], (self.x, self.y))
            #returns x coordinate. this will be used for triggering the minigame scenes
            return self.x
    
    #Creting Menu Object
    class BlueMenu():
        '''A class used for displaying menu in the overworld based on interaction'''
        global win
        #initiliazing values
        def __init__(self,num):
            self.menu = pygame.transform.scale(pygame.image.load('arcade_resources/bluemenu.png'), (95*7,59*7))         #menu
            self.pongmenu = pygame.transform.scale(pygame.image.load('arcade_resources/ponghub.png'), (95*7,59*7))      #controls for pong
            self.snakemenu = pygame.transform.scale(pygame.image.load('arcade_resources/snakehub.png'), (95*7,59*7))    #controls for snake
            self.flappymenu = pygame.transform.scale(pygame.image.load('arcade_resources/flappyhub.png'), (95*7,59*7))  #controls for flappy
            self.mastermenu = [self.snakemenu, self.pongmenu, self.flappymenu]
            self.menuindex = 0                                                                                          #the index of mastermenulist
            self.num = num                                                                                              #stores num value as self.num
            self.running = False                                                                                        #initializing running booean
            self.x = 32*7                                                                                               #x coordinates of  menu screen
            self.y = 17*7                                                                                               #y coordinates of menu screen
        #Master Menu Function For Displayin controls of Each Game
        def mastermenuboom(self):
            self.running = True
            while self.running:
                win.blit(self.mastermenu[self.menuindex], (self.x,self.y))
                for event in pygame.event.get():
                    if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.running = False
                pygame.display.update() 

        #Main Run Code for Menu and Triggering Game Scenes
        def runmenu(self):
            running = True
            while running:
                win.blit(self.menu, (self.x,self.y))                     #Blit the Play? Option Menu
                for event in pygame.event.get():                         #event loop
                    if event.type == QUIT:                                  
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False
                        if event.key == K_x:
                            if self.num == 1:                            #arcade 1
                                SnakeGame().run()
                                #GAME 1 
                            if self.num == 2:                            #arcade 2
                                # Playpong()
                                SpacePong_play()       
                                #GAME 2
                            if self.num == 3:                            #arcade 3
                                flappymain()
                                #GAME 3                                                      
                            running = False                              #running is false once minigames are exited    
                        if event.key == K_1:                             #if '1' is pressed then it will call the master menu function which will show controls of each specific game
                            self.menuindex = self.num-1
                            self.mastermenuboom()
                pygame.display.update() 
    

    #- - - - - - - - - - - - - - Functions for the overworld or the arcade - - - - - - - - - - - - -#
    # plays background music
    def play_background_music():    
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('arcade_resources/The search.mp3')
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(1)

    #returns which arcade box were 'interacted' with based on the x value of player
    def check_arcade(x):
        '''the values compared to x are the x coordinates of each arcade box'''
        arcade = 0
        if 38*7 <= x < 53*7 and x+11*7 < 53*7 and keys[pygame.K_e]:
            arcade = 1
        if 60*7 <= x < 75*7 and x+11*7 < 75*7 and keys[pygame.K_e]:
            arcade = 2
        if 82*7 <= x < 97*7 and x+11*7 <97*7 and keys[pygame.K_e]:
            arcade = 3
        if 104*7 <= x < 119*7 and x+11*7 < 119*7 and keys[pygame.K_e]:
            arcade = 4
        if 126*7 <= x< 141*7 and x+11*7 < 144*7 and keys[pygame.K_e]:
            arcade = 5
        return arcade
               
    #background blit = the animation function for blitting the background
    def background_blit():
        '''1000 ticks has passed then the background frame gets updated'''
        global last_update_bg, frame_bg
        current_time_bg = pygame.time.get_ticks()
        if current_time_bg - last_update_bg >= 1000:
            frame_bg += 1
            last_update_bg = current_time_bg
            if frame_bg >= 2:
                frame_bg = 0  
        win.blit(background_anim[frame_bg], (0,0))
    
    #arcadescreen blit - will blit a screen onto the arcade nepending on the num value taken from player object
    def blitblink(num):
        if num in (1,2,3,4,5):
            if num == 1:
                win.blit(blink, (43*7, 45*7))
            if num == 2:
                win.blit(blink, (65*7, 45*7))
            if num == 3:
                win.blit(blink, (87*7, 45*7))
            if num == 4:
                win.blit(blink, (109*7, 45*7))
            if num == 5:
                win.blit(blink, (131*7,45*7))

    #----------------------------------------- Main Game Loop -----------------------------------------------------------------------#
    #other variables in main() function#
    character = Player(14, 38)                      #Calling player object as character
    run = True                                      #for game loop
    while run:
        play_background_music()                     #play bg music

        keys = pygame.key.get_pressed()             #keys for keyboard presses
        time = pygame.time.get_ticks()              #sets time
        clock.tick(FPS)                             #sets fps of the game

        background_blit()                           #bliting background animation
        num = character.movement()                  #booleans for character movement and animation
        blitblink(num)                              #num means a character interacted with an arcade, so the arcade will be blitting
        x = character.draw(win)                     #updates character position and animation frame
        arcade = check_arcade(x)                    #checks which arcade box has been interacted with

        if arcade in (1,2,3):                       #if arcade box 1,2,3 were interacted with, prompts the blue menu
            BlueMenu(num).runmenu()

        for event in pygame.event.get():            #loop for taking events
            if event.type == pygame.QUIT:
                run = False  
                          
        pygame.display.update()                     #updates the display
    pygame.quit()

if __name__ == "__main__":
    main()