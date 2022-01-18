import pygame
from pygame.locals import *
import time
from random import randint

# block's dimensions are 70 x 70 px
size = 70

# dimensions of the game's window
surface_width = 1120
surface_length = 630


# class creates an apple for the snake
class Apple:
    def __init__(self, main_screen):
        self.main_screen = main_screen

        # loads image of apple
        image = pygame.image.load("snake_resources/apple.png").convert_alpha()

        # scales the dimensions of image to 70 x 70 px
        self.image = pygame.transform.scale(image, (70, 70))

        # coordinates of the apple are random
        self.x = randint(0, surface_width // size - 1) * size  # subtracting 1 from range prevents apple from
        self.y = randint(0, surface_length // size - 1) * size  # spawning outside the game window

    # method draws the apple on random location
    def draw(self):
        self.main_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    # will move the apple to a different random location upon contact with snake
    def move(self):
        self.x = randint(0, surface_width // size - 1) * size
        self.y = randint(0, surface_length // size - 1) * size


# class creates the snake
class Snake:
    def __init__(self, main_screen, length):
        self.main_screen = main_screen
        image = pygame.image.load("snake_resources/block.png").convert_alpha()
        self.block = pygame.transform.scale(image, (70, 70))

        # snake is stationary at the beginning
        self.direction = 'none'

        # describes how long the snake is currently
        self.length = length  # score is derived by subtracting one from length

        # starting position is at x = 70 and y = 70
        self.x, self.y = [size], [size]

    # updates the window to prevent multiple "snakes" from appearing
    def draw(self):
        # draws snake parts as length increases
        for i in range(self.length):
            self.main_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    # ff. four methods are the directions the snake can move in
    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    # describes how snake moves
    def walk(self):

        # for loop iterates through the "parts" of the snake
        for i in range(self.length - 1, 0, -1):  # starts with the last part of the snake and ends just before the head

            # as the snake moves, each part takes the coordinates of the part that precedes it
            self.x[i] = self.x[i - 1]  # for ex. the second part/block will take the place of where the head was
            self.y[i] = self.y[i - 1]

        # if statements change the x or y coordinates depending on the direction
        if self.direction == 'up':
            self.y[0] -= size  # we don't add because the positive y coordinates are at the bottom of the window
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size

        # we always draw the snake regardless of direction
        self.draw()

    # used later when snake eats apple and grows
    def increase_length(self):
        self.length += 1

        # appending elements to the two lists allows snake to grow
        self.x.append(-1)
        self.y.append(-1)


class SnakeGame:
    # function plays the background music and sets volume
    def play_background_music(self, volume):
        pygame.mixer.music.load("snake_resources/background_music.mp3")

        # background music loops indefinitely
        pygame.mixer.music.play(loops=-1)

        pygame.mixer.music.set_volume(volume)

    # function plays sounds when score increases or game over conditions are satisfied
    def play_sound(self, sound, volume):
        sound = pygame.mixer.Sound("snake_resources/%s.mp3" % sound)
        pygame.mixer.Sound.play(sound)
        sound.set_volume(volume)

    def __init__(self):

        # initialize pygame and mixer modules
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("SNAKE")

        self.play_background_music(volume=0.35)

        # initialize a window for display
        self.display_surface = pygame.display.set_mode(size=(surface_width, surface_length))

        # initialized window becomes our main screen where we draw our snake and apple
        self.snake = Snake(self.display_surface, 1)  # creates a snake of length 1
        self.snake.draw()

        # creates apple
        self.apple = Apple(self.display_surface)
        self.apple.draw()

    # displays current score
    def display_score(self):
        font = pygame.font.SysFont('robotoblack', size=40)
        score = font.render("Score: %d" % (self.snake.length - 1), True, (255, 255, 255))  # score is snake length - 1

        # value helps in arranging the position of current score
        score_width = score.get_width()
        self.display_surface.blit(score, (surface_width - score_width - size//2, 10))

    # collision logic
    def collision(self, x1, y1, x2, y2):  # used when snake eats an apple or itself
        if x2 <= x1 < x2 + size:
            if y2 <= y1 < y2 + size:
                return True
        return False

    def render_background(self):
        background = pygame.image.load("snake_resources/background_image.jpg")
        scaled_background = pygame.transform.scale(background, (surface_width, surface_length))
        self.display_surface.blit(scaled_background, (0, 0))

    def play(self):
        self.render_background()

        # snake will move automatically once the player presses one of the arrow keys
        self.snake.walk()

        self.apple.draw()

        self.display_score()

        pygame.display.flip()

        # executes if snake comes into contact with apple
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("score_up", volume=0.35)
            self.snake.increase_length()  # snake grows and score increases by 1
            self.apple.move()  # apple spawns randomly again

        # executes if snake comes into contact with itself
        for i in range(2, self.snake.length):  # it's possible for snake to eat itself at length 3

            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                # two separate sounds play
                self.play_sound("snake_eats_self", volume=1)
                time.sleep(1)
                self.play_sound("game_over", volume=0.75)

                # necessary for displaying final score and resetting the game
                raise "Game Over"

        # executes if snake goes beyond the boundaries of the game's window
        if not (0 <= self.snake.x[0] <= surface_width and 0 <= self.snake.y[0] <= surface_length):
            self.play_sound("bonk", volume=1)
            time.sleep(1)
            self.play_sound("game_over", volume=0.75)

            raise "Game Over"

    # displays final score
    def game_over(self):
        # game over screen
        self.render_background()

        font = pygame.font.SysFont('robotoblack', 40)

        # lines display final score and a message for the player
        final_score = font.render("Final Score: %d" % (self.snake.length - 1), True, (255, 255, 255))
        message = font.render("Press 'Enter' to play again or 'Esc' to exit to the arcade", True, (255, 255, 255))

        final_score_width = final_score.get_width()
        msg_width = message.get_width()

        # places the lines around upper center area of window
        self.display_surface.blit(final_score, (surface_width / 2 - final_score_width / 2, surface_length / 3 - size))
        self.display_surface.blit(message, (surface_width / 2 - msg_width / 2, surface_length / 3))
        pygame.display.flip()

        # background music is paused in game over screen
        pygame.mixer.music.pause()

    # shows when pause = True
    def pause_screen(self):
        font = pygame.font.SysFont('robotoblack', 80)
        pause_msg = font.render("PAUSED", True, (255, 255, 255))

        pause_msg_width = pause_msg.get_width()
        self.display_surface.blit(pause_msg, (surface_width / 2 - pause_msg_width / 2, surface_length / 3 - size))

        pygame.display.flip()
        pygame.mixer.music.pause()

    # determines how fast the snake is moving
    def snake_speed(self):

        # snake gets faster as score increases
        if self.snake.length <= 60:
            time.sleep(0.20 - ((self.snake.length //10) * 0.01))

        # speed cap at score 60
        else:
            time.sleep(0.1)

    # resets the game
    def reset(self):
        self.snake = Snake(self.display_surface, 1)
        self.apple = Apple(self.display_surface)

    def run(self):

        # exits game when running becomes False
        running = True

        # game's default is 'unpaused'
        pause = False

        # while loop becomes event loop
        while running:

            # loop iterates through event queue
            for event in pygame.event.get():

                # executes if a key is pressed down
                if event.type == KEYDOWN:

                    # exits the game when pressing ESC
                    if event.key == K_ESCAPE:
                        running = False
                        pygame.mixer.music.stop()

                    # enter key resets the game from the game over screen
                    if event.key == K_RETURN:
                        if not pause:
                            self.pause_screen()
                            pause = True
                        elif pause:
                            pygame.mixer.music.unpause()
                            pause = False

                    # arrow key input is processed when game is unpaused
                    if not pause:

                        # '!=' operator ensures that the snake can't turn to the opposite of its current direction
                        if event.key == K_UP and self.snake.direction != 'down':
                            self.snake.move_up()

                        if event.key == K_DOWN and self.snake.direction != 'up':
                            self.snake.move_down()

                        if event.key == K_LEFT and self.snake.direction != 'right':
                            self.snake.move_left()

                        if event.key == K_RIGHT and self.snake.direction != 'left':
                            self.snake.move_right()

                # exits game when pressing the window's 'X' button
                elif event.type == QUIT:
                    running = False
                    pygame.mixer.music.stop()

            try:

                if not pause:
                    self.play()

            # executes when snake crashes into itself or the boundaries
            except Exception:
                self.game_over()

                # ignores input from arrow keys and stops 'play' method in the try block above
                pause = True

                self.reset()

            self.snake_speed()

