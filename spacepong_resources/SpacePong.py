#Final Ping Pong Game

#importing necessary module for game design
import turtle
import pygame
import time
from pygame import mixer

# Pause variable
is_paused = False
# running variable
running = True

# Quit variable
game_quit = False
# running variable
game_run = False

def toggle_pause():
    global is_paused
    if is_paused == True:
        is_paused = False
    else:
        is_paused = True

def toggle_exit():
    global running
    running = False

def SpacePong_play():
    #Main Screen
    bg = turtle.Screen()    #setting mainscreen using .Screen() function
    bg.title("Space-Pong!")  #
    bg.bgcolor("Black")
    bg.setup(width=1120, height=630)    #setting the screen resolution
    bg.tracer(0)    #setting off the screen updates
    bg.bgpic("SpacePong_bg.gif")    

    #Applying Background Music
    pygame.mixer.init() #pygame funtion for mixer initialization, ensures that the music plays
    mixer.music.load('background_music.wav')    #importing the music file from local directory
    mixer.music.play(-1)    #setting the music runtime to -1 to secure contiuous playing

    #court separator - draws a line to indicate respectie courts
    border = turtle.Turtle()    #funtion call to create an object, border in this case (1st game object)
    border.speed(0) #indicates the animation speed, ensures that there will be no animation delays
    #implementing object design
    border.shape("square")
    border.color("white")
    border.shapesize(stretch_wid=24.5, stretch_len=0.1)
    border.goto(0,-65)  #object coordinates

    #Initial Scores - assigning initial values to players' scores
    #necessary integer values for latter operations on score increase 
    player_1_score = 0
    player_2_score = 0

    #left paddle (player A)
    APaddle = turtle.Turtle()   #treating APaddle as an object (2nd game object)
    APaddle.speed(0)    #animation speed, ensures that there are no delays
    #paddle designs : shape, color, size
    APaddle.shape("square")
    APaddle.color("white")
    APaddle.shapesize(stretch_wid=4, stretch_len=1) #smaller paddle for extra challenge xD
    APaddle.penup() #used to make the paddle not to create lines when moving
    APaddle.goto(-500,-60)  #paddle coordinates
    APaddlexdirection = 0   #applyig 0 initial motion to the paddle

    #left paddle (player B)
    BPaddle = turtle.Turtle()     #treating BPaddle as an object (3rd game object)
    BPaddle.speed(0)    #setting animation speed to 0, ensuring that there will be no delays
    #implementing designs on the paddle : shape, color, size
    BPaddle.shape("square")
    BPaddle.color("white")
    BPaddle.shapesize(stretch_wid=4, stretch_len=1)
    BPaddle.penup() #esnuring lines will not appear when the paddle moves
    BPaddle.goto(500,-60)   #paddle coordiates, inverse coordinate of APaddle
    BPaddlexdirection = 0   #applying 0 initial motion to the paddle

    #ball
    ball = turtle.Turtle()  #treating ball as an object (4th game object)
    ball.speed(0)   #animation speed set to 0
    #implementing object deisgns
    ball.shape("circle")
    ball.color("red")
    ball.penup()    #getting rid of lines when moving
    ball.goto(0, -60)   #ball coordinate
    ballxdirection = 2   #applying motion in x direction, speed set to 0.75
    ballydirection = 2   #applying motion in y direction, speed set to 0.75  

    #creating title
    Gtitle = turtle.Turtle()    #treating Gtitle as an object (5th game object)
    Gtitle.speed(0) #setting animation speed to 0, removes delays
    #implementing designs : shape, color, size
    Gtitle.color("white")
    Gtitle.penup()  #getting rid of unwanted lines 
    Gtitle.hideturtle() #makes the buil-in turtle logo invisible
    Gtitle.goto(0,230)  #object coordinates
    #using write fucntion to print texts, formatting it at the same time
    Gtitle.write("S  P  A  C  E  -  P  O  N  G", align="center",font=('Callibri', 48, 'bold'))

    #creating score card (Player A)
    Ascore = turtle.Turtle()    #treating Ascore as an object (6th game object)
    Ascore.speed(0) #setting animation speed to 0
    #implementing object designs 
    Ascore.color("white")
    Ascore.penup()  #removing unnecessary lines
    Ascore.hideturtle() #hiding the built-in turtle object
    Ascore.goto(-500,190)   #object coordinates
    #formatting text design
    Ascore.write("P L A Y E R  1 :  0", align="left",font=('Callibri', 24, 'bold'))

    #Ascore duplicate placed in a mirror coordinate
    #creating score card (Player B)
    Bscore = turtle.Turtle()    #(7th game object)
    Bscore.speed(0)
    Bscore.color("white")
    Bscore.penup()
    Bscore.hideturtle()
    Bscore.goto(500,190)
    Bscore.write("P L A Y E R  2 :  0", align="right",font=('Callibri', 24, 'bold'))

    #creating a border line below the score cards
    Bline = turtle.Turtle() #treating Bline as a game object (8th game object)
    Bline.speed(0)  #setting animation speed to 0
    #implementing object design
    Bline.shape("square")
    Bline.color("white")
    Bline.shapesize(stretch_wid=0.1, stretch_len=96)
    Bline.penup()   #getting rid of unnecessary lines
    Bline.goto(0,180)   #object coordinate

    #duplicate of Bline in the lower floor coordinate
    #creating a border line below the score cards
    floor = turtle.Turtle()
    floor.speed(0)
    floor.shape("square")
    floor.color("white")
    floor.shapesize(stretch_wid=0.1, stretch_len=96)
    floor.penup()
    floor.goto(0,-310)

    #Upward Motion - APaddle
    def APaddle_upward():
        y = APaddle.ycor()  #ycor() returns the y coordinate
        y += 40 #sets movement of the paddle to 20px when moving in the + y-axis
        APaddle.sety(y) #setting new y coordinate

    #Downward motion - APaddle
    def APaddle_downward():
        y = APaddle.ycor()  #ycor() returns the y coordinate
        y -= 40 #sets the movement of the paddle to 20px when moving in the - y-axis
        APaddle.sety(y) #setting the new y coordinate

    #implementing the same movement structure to the second paddle
    #Upward motion - BPaddle
    def BPaddle_upward():
        y = BPaddle.ycor()
        y += 40
        BPaddle.sety(y)

    #Downward motion - BPaddle
    def BPaddle_downward():
        y = BPaddle.ycor()
        y -= 40
        BPaddle.sety(y)

    #stops all the playing music
    def stop_music(x):
        mixer.music.stop()

    #plays the winner effect
    def end_sound():
        winner_effect = mixer.Sound('winner_effect.wav')
        winner_effect.play()
    
    #defining end game
    def toggle_end():
        if player_2_score < player_1_score:
            end_sound() #plays the function play the end sound
            bg.clear()  #clears every element in the screen
            bg.reset()  #resets the main screen to none
            bg.bgpic("player_1_effect.gif") #displays the winner image
            mixer.music.stop()  #stops the bg music
            stop_music(paddle_sound)
            stop_music(score_sound)
            stop_music(bounce_sound)
            
        #urtilizing same measurements and ideas, except a different image is presented
        elif player_1_score < player_2_score:
            end_sound()
            bg.clear()
            bg.reset()
            bg.bgpic("player_2_effect.gif")
            mixer.music.stop()
            stop_music(paddle_sound)
            stop_music(score_sound)
            stop_music(bounce_sound)
            
        else:
            end_sound()
            bg.clear()
            bg.reset()
            bg.bgpic("game_over_effect.gif")
            mixer.music.stop()
            stop_music(paddle_sound)
            stop_music(score_sound)
            stop_music(bounce_sound)
            

    #navigating keys for paddle movement trigger
    bg.listen() #commands the program to accept user connections
    bg.onkeypress(APaddle_upward, 'w') or bg.onkeypress(APaddle_upward, 'W')    #assigning a key for upward movement (player 1)
    bg.onkeypress(APaddle_downward, 's') or bg.onkeypress(APaddle_downward, 'S')    #assigning a key for downward movement (player 1)
    bg.onkeypress(BPaddle_upward, 'Up') #assigning a key for upward movement (player 2)
    bg.onkeypress(BPaddle_downward, 'Down') #assigning a key for downward movement (player 2)
    bg.onkeypress(toggle_pause,'Return')
    bg.onkeypress(toggle_exit, 'Escape')
    bg.onkeypress(toggle_end, 'e') or bg.onkeypress(toggle_end, 'E')

    while running:
        bg.update()
        if not is_paused:
            #applying motion to the ball
            #applying motion to the ball
            ball.setx(ball.xcor()+ballxdirection)
            ball.sety(ball.ycor()+ballydirection)

                #border set up (for the paddles)
            if APaddle.ycor()>130:
                APaddle.sety(130)
                APaddlexdirection*= 0   #limits the movement of the paddle once it reaches the set border limit in the positive y-axis

            if APaddle.ycor()<-260:
                APaddle.sety(-260)
                APaddlexdirection *= 0  #limits the movement of the paddle once it reaches the set border limit in the negative y-axis

            #applies the same measurement as the first paddle to keep them uniform    
            if BPaddle.ycor()>130:
                BPaddle.sety(130)
                BPaddlexdirection *= 0

            if BPaddle.ycor()<-260:
                BPaddle.sety(-260)
                BPaddlexdirection *= 0
                  
            #border set up (for the ball)
            if ball.ycor()>172:
                ball.sety(172)  #utilizing the same y-coordinate as the borderline below the score cards
                ballydirection *= -1    #reverses the ball direction when condition is met
                bounce_sound = mixer.Sound('bounce_effect.wav') #imports the music file from the local directory through the mixer
                bounce_sound.play() #commands the program to play the sound

            if ball.ycor()<-300:
                ball.sety(-300) #utilizing the same y-coordinate as the floor borderline
                ballydirection *= -1    #reverses the ball direction when ccondition is met
                bounce_sound = mixer.Sound('bounce_effect.wav') #imports the music file from the local directory through the mixer
                bounce_sound.play() #commands the program to play the sound

            if ball.xcor()>570: #x coordinate pass the x coordinate of BPaddle
                ball.goto(0, -60)   #ball goes back to center 
                ballxdirection *= -1    #reverses the ball direction
                player_1_score += 1     #adds 1 to player 1 score
                Ascore.clear()  #clears the initial text written on Player 1's score card
                Ascore.write("P L A Y E R  1 :   {}".format(player_1_score, None),align="left",font=('Ugly Byte', 24, 'bold'))  #formats the player's score storing it in the {}
                score_sound = mixer.Sound('score_effect.wav')   #imports the music file from the local directory
                score_sound.play()  #plays the locally imported music file
            
            #utilizes the same measurements as player A's score card, just located on the mirror coordinate
            if ball.xcor()<-570:
                ball.goto(0,-60)
                ballxdirection *= -1
                player_2_score += 1
                Bscore.clear()
                Bscore.write("P L A Y E R  2 :   {}".format(player_2_score, None), align="right",font=('Ugly Byte', 24, 'bold'))
                score_sound = mixer.Sound('score_effect.wav')
                score_sound.play()

            #Executing ball-paddle collisions 

            #commands the ball to react when hits the coordinate a few units before the BPaddle coordinate
            if (ball.xcor() > 480 and ball.xcor() < 520) and (ball.ycor() < BPaddle.ycor() + 60 and ball.ycor() > BPaddle.ycor() - 60): 
                ball.setx(480)  #sets the new x coordinate, the maximum the ball can reach when interacted with the paddle
                ballxdirection *= -1    #reverses the direction
                paddle_sound = mixer.Sound('paddle_effect.wav') #imports the music file form local directory
                paddle_sound.play() #plays the imported music file

            #utilizes the same condition and response from the right paddle, only this is located on the mirror coordinate of the other
            if (ball.xcor() < -480 and ball.xcor() > -520) and (ball.ycor() < APaddle.ycor() + 60 and ball.ycor() > APaddle.ycor() - 60):
                ball.setx(-480)
                ballxdirection *= -1
                paddle_sound = mixer.Sound('paddle_effect.wav')
                paddle_sound.play() 
        else:
            bg.update()
SpacePong_play()
