import pygame
import random
import state

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
        self.pixels = create_grid()
        self.buffer = [0] * (64 * 32)
        self.screen.fill("purple")
        pygame.display.set_caption("Chip8 Emulator")


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
        while state.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state.game_running = False
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
        self.off_colour, self.on_colour = state.themes[state.selected_theme]

        state.game_running = True

    def randomise(self):
        self.state = random.random() < 0.5
    
    def draw(self, surface):
        if self.state: 
            self.colour = self.on_colour
        else:
            self.colour = self.off_colour
        
        pygame.draw.rect(surface, self.colour, self.rect)


class ThemeManager:
    def __init__(self, selected_theme="classic"):
        self.selected_theme = selected_theme

        # THEMES
        self.classic = ("black", "white")
        self.hacker = ("black", "green")

        self.theme_names = {
            "classic": self.classic,
            "hacker": self.hacker
            }

        # actiavte the selected theme
        theme_colours = self.theme_names.get(self.selected_theme, self.classic)
        self.off_colour, self.on_colour = theme_colours
        
    def report_selected_colours(self):
        return self.off_colour, self.on_colour

