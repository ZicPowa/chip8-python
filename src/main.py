# src/main.py: create Memory, CPU, Display, and run the emulation loop.
import display
from memory import Memory
from cpu import CPU
from keyboard import Keyboard

ram = Memory()
ram.load_fontset()
ram.load_rom()
ram.dump(True)

display1 = display.Display()
cpu = CPU(ram.data, display1)
display1.run() 

"""
# main.py - the emulation loop
while running:
    # 1. Handle input (non-blocking)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Run ~10 CPU instructions (≈ 600 Hz at 60 FPS)
    for _ in range(10):
        cpu.cycle()  # fetch → decode → execute one opcode

    # 3. Decrement timers at 60 Hz
    cpu.tick_timers()

    # 4. Draw the current framebuffer state
    display.draw()

    # 5. Cap at 60 FPS — this is what sets the pace
    clock.tick(60)
"""