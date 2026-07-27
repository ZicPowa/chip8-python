# src/main.py: create Memory, CPU, Display, and run the emulation loop.
import display
from memory import Memory
from cpu import CPU
from keyboard import Keyboard

# Add the path to your rom here: 
rom_path = "test_roms/space_invaders.ch8"

ram = Memory(rom_path)
ram.load_fontset()
ram.load_rom()
ram.dump(True)
keyboard1 = Keyboard()
display1 = display.Display(keyboard1)
cpu1 = CPU(ram.data, display1, keyboard1)
display1.run(cpu1) 
