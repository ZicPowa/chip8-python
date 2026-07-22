# src/main.py: create Memory, CPU, Display, and run the emulation loop.
import display
from memory import Memory
from cpu import CPU

ram = Memory()
ram.load_fontset()
ram.load_rom()
ram.dump(True)

display1 = display.Display()
cpu = CPU(ram.data, display1)
display1.run() 
