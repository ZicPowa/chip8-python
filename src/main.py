'''
src/main.py: create Memory, CPU, Display, and run the emulation loop.
'''

from memory import Memory
from cpu import CPU

ram = Memory()
ram.load_fontset()
ram.load_rom()
ram.dump(True)

cpu = CPU(ram.data)