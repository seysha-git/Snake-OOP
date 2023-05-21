import pygame
from pygame.locals import *
import time
import settings
import random

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("./Snake/resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = settings.SIZE * 3
        self.y = settings.SIZE * 3
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()# It allows only a portion of the screen to be updated, instead of the entire area.
    def move(self):
        self.x = random.randint(0,22)*settings.SIZE
        self.y = random.randint(0, 18)*settings.SIZE


class Snake:
    def __init__(self, parent_screen, length):
        #Instance variables
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("./Snake/resources/block.jpg").convert()
        #Setting the snake shape by duplicating the SIZE with an given length
        self.x = [settings.SIZE]*length
        self.y = [settings.SIZE]*length
        self.direction = "down"

    def increment_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    def draw(self):
        self.parent_screen.fill((settings.BACKGROUND))#for each time you are moving, you update the screen so that you dont see previous block
        for i in range(self.length):#
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))#setting the position with index of the snake_length
        pygame.display.flip()# It allows only a portion of the screen to be updated, instead of the entire area.
    #The four methods below moves the snake
    def walk(self):
        """
        The shift of the positions of the blocks in reverse order in the walk method of the Snake 
        class is achieved through a loop that iterates over the range of the snake's length, 
        starting from the second-to-last block index and moving backwards to the first block index (0).

        Within this loop, each block's position is updated to match the position of the preceding block. 
        This is done by assigning the x and y coordinates of the current block (self.x[i] and
        self.y[i]) with the values of the x and y coordinates of the preceding block (self.x[i-1] and self.y[i-1]).

        By shifting the positions in reverse order, the blocks of the snake essentially follow the position of the preceding block,
        allowing the snake to appear as if it is moving forward and creating the illusion of continuous motion.
        """
        for i in range(self.length-1, 0, -1):#Loops the length from oposite direction
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == "up":
            self.y[0] -= settings.SIZE
        if self.direction == "down":
            self.y[0] += settings.SIZE
        if self.direction == "left":
            self.x[0] -= settings.SIZE
        if self.direction == "right":
            self.x[0] += settings.SIZE
            
        self.draw()
    def move_left(self):
        self.direction = "left"
    def move_right(self):
        self.direction = "right"
    def move_up(self):
        self.direction = "up"
    def move_down(self):
        self.direction = "down"
    

class Game:
    def __init__(self):
        pygame.init() #initiali<e game
        self.surface = pygame.display.set_mode((1000, 800))
        pygame.mixer.init()
        self.surface.fill(settings.BACKGROUND)
        self.snake = Snake(self.surface, 1)#self.surface becomes parent_screen in Snake class
        self.snake.draw()#Look line 12
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.play_background_music()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + settings.SIZE:
            if y1 >= y2 and y1 < y2 + settings.SIZE:
                return True
        return False
    
    def play_background_music(self):
        pygame.mixer.music.load('./Snake/resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, soundName):
        sound = pygame.mixer.Sound(f"./Snake/resources/{soundName}.mp3")
        pygame.mixer.Sound.play(sound)

    
    def play(self): 
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake collding with apple

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
           self.play_sound("ding")
           self.snake.increment_length()
           self.apple.move()
        #snake collding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"

    def display_score(self):
        font = pygame.font.SysFont(settings.FONT_TYPE, 20)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (800, 10))
    def show_game_over(self):
        self.surface.fill(settings.BACKGROUND)
        font = pygame.font.SysFont(settings.FONT_TYPE, 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()

        pass
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                #Event type refers to the press key on the keyboard
                if event.type == KEYDOWN: # if a key is pessed
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:    
                    running = False
            try:
                if not pause:
                  self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            #it "rewalks" every 0.2 seconds
            time.sleep(.2)

 

if __name__ == "__main__":
    game = Game()
    game.run()
   

    