import pygame
import time
import random
from pygame.locals import *


"""
    TO DO
    1. Blocks that line up to grid --- Written, needs testing
    2. Not hardcoded start positions --- Written, Tested
    3. Game over screen with score and play again / exit
    4. Other kinds of pickups
    5. Bigger window / smaller snakes
    6. More playable snake speed (slower)
"""


class Snake:
    """
    This object represents the snake that each player controls.
    """
    def __init__(self, length=3, speed=40, direction='left',x_start=10,y_start=10):
        """
        The default parameters are as such:
        length = 3 like in classic snake, but I made it longer to demonstrate lack of collision.
        speed = the size of the block, so that the snake moves one unit at a time.
        direction = 'down' so that the snake doesn't immidiately crash.
        I might want to add initial x and y positions as parameters as well,
        otherwise the snake always starts in the upper left corner with its tail pointed right.
        """
        self.x = []
        self.y = []
        self.length = length # Number of boxes of snake
        self.speed = speed # Movement per lurch - the snake is start-stop.
        self.direction = direction # str, right/left/up/down

        self.x.append(x_start)
        self.y.append(y_start)

        """
        Initializes the snake as a horizontal row of blocks.
        Since the snake moves one block per lurch, each block is one multiple of speed behind the last.
        The if statements are so that the tail is pointed out behind the snake.
        """
        if self.direction == 'left':
            for i in range(self.length):
                self.x.append(x_start + self.speed * i)
                self.y.append(y_start)

        if self.direction == 'right':
            for i in range(self.length):
                self.x.append(x_start - self.speed * i)
                self.y.append(y_start)

    # These functions set direction when called
    # I thought about making direction an object, but it really only needs one piece of information
    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction ='left'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    # surf.blit is taken from a pygame tutorial
    def draw(self,surf,image):
        for i in range(self.length):
            surf.blit(image,(self.x[i],self.y[i]))

    """
    This function adds a block to the snake. The new block is at the same location
    as the tip of the tail, but when the snake next moves it shifts to the correct
    location. This gives the appearence of the tail freezing for a second.
    """
    def grow(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    def update(self):
        """
        This changes position based on direction.
        """

        #This part moves each block to the position of the block ahead of it
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # This changes x and y based on speed and direction
        if self.direction == 'right':
            self.x[0] += self.speed
        if self.direction == 'left':
            self.x[0] -= self.speed
        if self.direction == 'up':
            self.y[0] -= self.speed
        if self.direction == 'down':
            self.y[0] += self.speed


class Food:
    """
    This class represents any of the pickups in the game.
    """
    def __init__(self, x, y, size=40):
        self.x = x
        self.y = y
        self.size = size

    # draw works the same way it does for the snake.
    def draw(self,surf,image):
        surf.blit(image,(self.x,self.y))

    """
    This moves the block to a new place on the screen.
    It divides by size, randomizes, then multiplies by size.
    This is to keep the block at an even space in the grid.
    """
    def update(self, width, height):
        self.x = random.randint(0,(width - self.size)/self.size)*self.size
        self.y = random.randint(0,(height - self.size)/self.size)*self.size


class Game:
    """
    This class is the game window itself, which will contain the snakes.
    """
    def __init__(self):
        self.running = True
        self.display_surf = None
        self.image_surf = None
        self.window_width = 1600
        self.window_height = 1200

        # Two snakes and an apple
        self.player1 = Snake(length=3, direction = 'left', x_start=self.window_width*2/3, y_start=self.window_height*2/3)
        self.player2 = Snake(length=3, direction = 'right', x_start=self.window_width/3, y_start=self.window_height/3)
        self.apple = Food(x=self.window_width/2, y=self.window_height/2)

    def play(self):
        """
        This entire class just has one function outsied of init.
        This is the function that makes the game do the thing.
        """
        pygame.init() #Gets pygame going
        # display_surf and image_surf are also from a pygame tutorial
        self.display_surf = pygame.display.set_mode((self.window_width,self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('Snakes on Bikes in PyGame')
        self.running = True
        self.image_surf1 = pygame.image.load('block.jpg').convert() # If I need to change an icon, do it here
        self.image_surf2 = pygame.image.load('block2.jpg').convert() # There is a separate image_surf for each player
        self.image_surf3 = pygame.image.load('apple.jpg').convert() # This is for the foods

        while self.running:
            pygame.event.pump() # This line is black magic:

            # This listens for the exit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            # This is a backup quit method using the escape key
            if (keys[K_ESCAPE]):
                self.running = False

            #These are all basic key listeners for the arrow keys for player 1
            if (keys[K_RIGHT]):
                self.player1.move_right()

            if (keys[K_LEFT]):
                self.player1.move_left()

            if (keys[K_UP]):
                self.player1.move_up()

            if (keys[K_DOWN]):
                self.player1.move_down()

            #These are the same thing, but for WASD keys for player 2
            if (keys[K_d]):
                self.player2.move_right()

            if (keys[K_a]):
                self.player2.move_left()

            if (keys[K_w]):
                self.player2.move_up()

            if (keys[K_s]):
                self.player2.move_down()


            #Calls the main function from the Snake class for each player
            self.player1.update()
            self.player2.update()

            # Check if player 1 collides with itself
            for i in range(1,self.player1.length):
                    if abs(self.player1.x[0] - self.player1.x[i]) < 40 and abs(self.player1.y[0] - self.player1.y[i]) < 40:
                        self.running = False

            # Check if player 2 collides with itself
            for i in range(1,self.player2.length):
                    if abs(self.player2.x[0] - self.player2.x[i]) < 40 and abs(self.player2.y[0] - self.player2.y[i]) < 40:
                        self.running = False

            # Check if player 1 collides with player 2
            for i in range(1,self.player2.length):
                    if abs(self.player1.x[0] - self.player2.x[i]) < 40 and abs(self.player1.y[0] - self.player2.y[i]) < 40:
                        self.running = False

            # Check if player 2 collides with player 1
            for i in range(1,self.player1.length):
                    if abs(self.player2.x[0] - self.player1.x[i]) < 40 and abs(self.player2.y[0] - self.player1.y[i]) < 40:
                        self.running = False

            # Player 1 Wall collision
            if self.player1.x[0] < 0:
                self.running = False
            if self.player1.y[0] < 0:
                self.running = False
            if self.player1.x[0] > self.window_width:
                self.running = False
            if self.player1.y[0] > self.window_height:
                self.running = False

            #Player 2 Wall collision
            if self.player2.x[0] < 0:
                self.running = False
            if self.player2.y[0] < 0:
                self.running = False
            if self.player2.x[0] > self.window_width:
                self.running = False
            if self.player2.y[0] > self.window_height:
                self.running = False

            if abs(self.player1.x[0] - self.apple.x) < 40 and abs(self.player1.y[0] - self.apple.y) < 40:
                self.player1.grow()
                self.apple.update(self.window_width,self.window_height)
            if abs(self.player2.x[0] - self.apple.x) < 40 and abs(self.player2.y[0] - self.apple.y) < 40:
                self.player2.grow()
                self.apple.update(self.window_width,self.window_height)


            self.display_surf.fill((0,0,0)) # Color! Right now its black
            self.player1.draw(self.display_surf, self.image_surf1)
            self.player2.draw(self.display_surf, self.image_surf2)
            self.apple.draw(self.display_surf, self.image_surf3)
            pygame.display.flip() # This line is also sorcery
            time.sleep(0.1) # Makes the game go human speed instead of computer speed

        #pygame.quit() # Once running = false, the program gets here and stops
        game1 = Game()
        game1.play()
if __name__ == "__main__":
    game = Game()
    game.play()
