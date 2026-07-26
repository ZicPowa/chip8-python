import pygame
import random # for testing

#setup
scaling_factor = 10
DEFAULT_WIDTH = 64 * scaling_factor
DEFAULT_HEIGHT = 32 * scaling_factor

def create_grid(cols=64, rows=32):
    return [[Pixel(x, y, scaling_factor) for x in range(cols)] for y in range(rows)]

class Display:
    def __init__(self, keyboard):
        pygame.init()
        self.keyboard = keyboard
        self.screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pixels = create_grid()
        self.buffer = [0] * (64 * 32)
        self.screen.fill("purple")

    def clear(self):
        self.buffer = [0] * (64 * 32)
        for row in self.pixels:
            for pixel in row:
                pixel.state = False
                pixel.colour = 'black'

    def update_from_buffer(self):
        for i, bit in enumerate(self.buffer):
            y, x = divmod(i, 64)
            self.pixels[y][x].state = bool(bit)

    def run(self, cpu):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.keyboard.check_key_down(event)

            for _ in range(10):
                cpu.cycle()
            cpu.tick_timers()

            self.update_from_buffer()
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
        self.state = 0
        self.former_state = self.state
        self.scaling_factor = scaling_factor
        self.rect = pygame.Rect(x*self.scaling_factor, y*self.scaling_factor, self.scaling_factor, self.scaling_factor)
        self.colour = 'black'

    def update_state(self):
        if self.former_state != self.state:
            self.former_state = self.state
            # pass this particular object as needing to be redrawn
            # TO DO!!!

    def randomise(self):
        self.state = random.random() < 0.5
    
    def draw(self, surface):
        if self.state: 
            self.colour = 'white'
        else:
            self.colour = 'black'
        
        pygame.draw.rect(surface, self.colour, self.rect)
