import pygame
import random # for testing

#setup
scaling_factor = 10
DEFAULT_WIDTH = 64 * scaling_factor
DEFAULT_HEIGHT = 32 * scaling_factor

def create_grid(cols=64, rows=32):
    return [[Pixel(x, y, scaling_factor) for x in range(cols)] for y in range(rows)]

class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pixels = create_grid()
        self.screen.fill("purple")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            for row in self.pixels:
                for pixel in row:
                    pixel.draw(self.screen)
            
            pygame.display.flip()  # puts work on screen
            self.clock.tick(60)

        pygame.quit()

class Pixel:
    def __init__(self, x, y, scaling_factor):
        self.x = x
        self.y = y
        self.state = random.random() < 0.5 # sets true or false randomly
        self.former_state = self.state
        self.scaling_factor = scaling_factor
        self.rect = pygame.Rect(x*self.scaling_factor, y*self.scaling_factor, self.scaling_factor, self.scaling_factor)
        self.colour = 'black'

    def update_state(self):
        if self.former_state != self.state:
            self.former_state = self.state
            # pass this particular object as needing to be redrawn
            # TO DO!!!
    
    def draw(self, surface):
        if self.state: 
            self.colour = 'white'
        else:
            self.colour = 'black'
        
        pygame.draw.rect(surface, self.colour, self.rect)
