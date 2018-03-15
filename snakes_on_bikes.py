import pygame
import time
import random
from pygame.locals import *


"""
    TO DO
    1. Blocks that line up to grid --- Done
    2. Not hardcoded start positions --- Done
    3. Game over screen with score and play again / exit --- Done
    4. Other kinds of pickups (If we have extra time)
    5. Bigger window / smaller snakes --- Bigger window
    6. More playable snake speed (slower) --- Tried, slower turns out to be less fun
"""


class Snake:
    """
    This object represents the snake that each player controls.
    """
    def __init__(self, length=3, speed=20, direction='left',x_start=10,y_start=10):
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
        if self.direction != 'left':
            self.direction = 'right'

    def move_left(self):
        if self.direction != 'right':
            self.direction ='left'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
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
    def __init__(self, x, y, size=20):
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
        self.window_height = 1000

        # This is the only place where this value needs to be changed in order to make the snake bigger or smaller
        self.block_size = 20

        # Two snakes and an apple
        self.player1 = Snake(length=5, direction = 'left', speed = self.block_size, x_start=self.window_width*2/3, y_start=self.window_height*2/3)
        self.player2 = Snake(length=5, direction = 'right', speed = self.block_size, x_start=self.window_width/3, y_start=self.window_height/3)
        self.apple1 = Food(x=self.window_width/2, y=self.window_height/2)
        self.apple2 = Food(x=self.window_width/4, y=self.window_height/2)
        self.apple3 = Food(x=self.window_width*3/4, y=self.window_height/2)

        # Initializing this now, but it doesn't get a real value until someone wins.
        self.winner = 0

    def play(self):
        """
        This entire class just has one function outside of init.
        This is the function that makes the game do the thing.
        """
        pygame.init() #Gets pygame going
        # display_surf and image_surf are also from a pygame tutorial
        self.display_surf = pygame.display.set_mode((self.window_width,self.window_height), pygame.HWSURFACE)
        self.running = True
        self.image_surf1 = pygame.image.load('blocksmall.jpg').convert() # If I need to change an icon, do it here
        self.image_surf2 = pygame.image.load('block2small.jpg').convert() # There is a separate image_surf for each player
        self.image_surf3 = pygame.image.load('applesmall.jpg').convert() # This is for the foods

        while self.running:
            pygame.event.pump() # This line is sorcery:

            # This listens for the exit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

            keys = pygame.key.get_pressed()

            # This is a backup quit method using the escape key
            if (keys[K_ESCAPE]):
                self.running = False
                pygame.quit()

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
                    if abs(self.player1.x[0] - self.player1.x[i]) < self.block_size and abs(self.player1.y[0] - self.player1.y[i]) < self.block_size:
                        self.running = False
                        self.winner = 2

            # Check if player 2 collides with itself
            for i in range(1,self.player2.length):
                    if abs(self.player2.x[0] - self.player2.x[i]) < self.block_size and abs(self.player2.y[0] - self.player2.y[i]) < self.block_size:
                        self.running = False
                        self.winner = 1

            # Check if player 1 collides with player 2
            for i in range(1,self.player2.length):
                    if abs(self.player1.x[0] - self.player2.x[i]) < self.block_size and abs(self.player1.y[0] - self.player2.y[i]) < self.block_size:
                        self.running = False
                        self.winner = 2

            # Check if player 2 collides with player 1
            for i in range(1,self.player1.length):
                    if abs(self.player2.x[0] - self.player1.x[i]) < self.block_size and abs(self.player2.y[0] - self.player1.y[i]) < self.block_size:
                        self.running = False
                        self.winner = 1

            # Player 1 Wall collision
            if self.player1.x[0] < 0:
                self.running = False
                self.winner = 2
            if self.player1.y[0] < 0:
                self.running = False
                self.winner = 2
            if self.player1.x[0] > self.window_width:
                self.running = False
                self.winner = 2
            if self.player1.y[0] > self.window_height:
                self.running = False
                self.winner = 2

            #Player 2 Wall collision
            if self.player2.x[0] < 0:
                self.running = False
                self.winner = 1
            if self.player2.y[0] < 0:
                self.running = False
                self.winner = 1
            if self.player2.x[0] > self.window_width:
                self.running = False
                self.winner = 1
            if self.player2.y[0] > self.window_height:
                self.running = False
                self.winner = 1

            if abs(self.player1.x[0] - self.apple1.x) < self.block_size and abs(self.player1.y[0] - self.apple1.y) < self.block_size:
                self.player1.grow()
                self.apple1.update(self.window_width,self.window_height)
            if abs(self.player2.x[0] - self.apple1.x) < self.block_size and abs(self.player2.y[0] - self.apple1.y) < self.block_size:
                self.player2.grow()
                self.apple1.update(self.window_width,self.window_height)

            if abs(self.player1.x[0] - self.apple2.x) < self.block_size and abs(self.player1.y[0] - self.apple2.y) < self.block_size:
                self.player1.grow()
                self.apple2.update(self.window_width,self.window_height)
            if abs(self.player2.x[0] - self.apple2.x) < self.block_size and abs(self.player2.y[0] - self.apple2.y) < self.block_size:
                self.player2.grow()
                self.apple2.update(self.window_width,self.window_height)

            if abs(self.player1.x[0] - self.apple3.x) < self.block_size and abs(self.player1.y[0] - self.apple3.y) < self.block_size:
                self.player1.grow()
                self.apple3.update(self.window_width,self.window_height)
            if abs(self.player2.x[0] - self.apple3.x) < self.block_size and abs(self.player2.y[0] - self.apple3.y) < self.block_size:
                self.player2.grow()
                self.apple3.update(self.window_width,self.window_height)


            self.display_surf.fill((0,0,0)) # Color! Right now its black
            self.player1.draw(self.display_surf, self.image_surf1)
            self.player2.draw(self.display_surf, self.image_surf2)
            self.apple1.draw(self.display_surf, self.image_surf3)
            self.apple2.draw(self.display_surf, self.image_surf3)
            self.apple3.draw(self.display_surf, self.image_surf3)
            pygame.display.flip() # This line is also sorcery
            time.sleep(0.05) # Makes the game go human speed instead of computer speed

        # pygame.quit() # Once running = false, the program gets here and stops

        """
        This section pulls up the scores which give the option to play again.
        """

        # Currently having some trouble with this text display part
        font1 = pygame.font.SysFont('Arial',30)

        # These have to be separate strings because \n doesn't work with blit.
        winner_message = 'PLAYER {} WON!'.format(self.winner)
        p1_message = 'PLAYER 1 LENGTH: {} BLOCKS'.format(self.player1.length)
        p2_message = 'PLAYER 2 LENGTH: {} BLOCKS'.format(self.player2.length)
        option_message = 'PRESS P TO PLAY AGAIN, X TO QUIT'

        # This puts each line of text into its own surface.
        text_surf_w = font1.render(winner_message,False,(255,255,255))
        text_surf_p1 = font1.render(p1_message,False,(255,255,255))
        text_surf_p2 = font1.render(p2_message,False,(255,255,255))
        text_surf_o = font1.render(option_message,False,(255,255,255))


        # This displays the text on the existing screen, right over the snakes.
        self.display_surf.blit(text_surf_w,(self.window_width/2-text_surf_w.get_width()/2, self.window_height/4-text_surf_w.get_height()/2))
        self.display_surf.blit(text_surf_p1,(self.window_width/2-text_surf_p1.get_width()/2, self.window_height/2-text_surf_p1.get_height()))
        self.display_surf.blit(text_surf_p2,(self.window_width/2-text_surf_p1.get_width()/2, self.window_height/2))
        self.display_surf.blit(text_surf_o,(self.window_width/2-text_surf_o.get_width()/2,self.window_height*3/4-text_surf_o.get_height()/2))

        # This part checks if the players want to play again or exit the game.
        for clock in range(600):
            # With 100 increments of time.sleep(0.1), this screen should stay up for 10 seconds.

            pygame.event.pump()

            # The code to quit is the same as in the loop above.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()

            # If they want to play another game, we simply call game again, overwriting the first version.
            if (keys[K_p]):
                game = Game()
                game.play()

            # If they want to exit the game.
            if (keys[K_x]):
                pygame.quit()

            # There might be a better way to keep this on the screen, but this works.
            time.sleep(0.1)

            pygame.display.flip()

        # If they don't pick anythin for a minute, meaning they probably left the game open
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.play()
