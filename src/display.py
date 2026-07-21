import pygame

#setup
scaling_factor = 12
DEFAULT_WIDTH = 64 * scaling_factor
DEFAULT_HEIGHT = 32 * scaling_factor


# setup
pygame.init()
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
clock = pygame.time.Clock()
running = True

while running:

    # poll for events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("purple")

    pygame.display.flip() # puts work on screen
    clock.tick(60)

pygame.quit()
