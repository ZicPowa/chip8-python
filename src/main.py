# src/main.py: create Memory, CPU, Display, and run the emulation loop.
import display
import state
from memory import Memory
from cpu import CPU
from keyboard import Keyboard
from gui import GUI

gui1 = GUI()
rom_name = gui1.run()

if rom_name is not None:
    rom_path = f"roms/{rom_name}"
    ram = Memory(rom_path)
    ram.load_fontset()
    ram.load_rom()
    ram.dump(True)
    keyboard1 = Keyboard()
    state.game_running = True
    display1 = display.Display(keyboard1)
    cpu1 = CPU(ram.data, display1, keyboard1)
    display1.run(cpu1)
