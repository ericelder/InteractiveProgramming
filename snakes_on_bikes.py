import pygame
import time
from pygame.locals import *

class Snake:
    """
    This object represents the snake that each player controls.
    """
    def __init__(self, length=3, speed=40, direction='down'):
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

        """
        Initializes the snake as a horizontal row of blocks.
        Since the snake moves one block per lurch, each block is one multiple of speed behind the last.
        """
        for i in range(self.length):
            self.x.append(self.speed * i)
            self.y.append(0)

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


class Game:
    """
    This class is the game window itself, which will contain the snakes.
    """
    def __init__(self):
        self.running = True
        self.display_surf = None
        self.image_surf = None
        self.windowWidth = 1200
        self.windowHeight = 900

        # Right now there's only one snake, but adding another shouldn't be too hard.
        self.player1 = Snake(length=12)

    def play(self):
        """
        This entire class just has one function outsied of init.
        This is the function that makes the game do the thing.
        """
        pygame.init() #Gets pygame going
        # display_surf and image_surf are also from a pygame tutorial
        self.display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Snakes on Bikes in PyGame')
        self.running = True
        self.image_surf = pygame.image.load('block.jpg').convert() # If I need to change an icon, do it here

        while self.running:
            pygame.event.pump() # This line is black magic:

            # This listens for the exit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            #These are all basic key listeners for the arrow keys.
            if (keys[K_RIGHT]):
                self.player1.move_right()

            if (keys[K_LEFT]):
                self.player1.move_left()

            if (keys[K_UP]):
                self.player1.move_up()

            if (keys[K_DOWN]):
                self.player1.move_down()

            # Right here is where WASD listeners could be added for player two

            self.player1.update() #Calls the main function from the Snake class
            self.display_surf.fill((0,0,0)) # Color! Right now its black
            self.player1.draw(self.display_surf, self.image_surf)
            pygame.display.flip() # This line is also sorcery
            time.sleep(0.1) # Makes the game go human speed instead of computer speed

        pygame.quit() # Once running = false, the program gets here and stops

if __name__ == "__main__":
    game = Game()
    game.play()