# memory.py
from pathlib import Path

default_fontset = [
    0xF0, 0x90, 0x90, 0x90, 0xF0, #0
    0x20, 0x60, 0x20, 0x20, 0x70, #1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, #2
    0xF0, 0x10, 0xF0, 0x10, 0xF0, #3
    0x90, 0x90, 0xF0, 0x10, 0x10, #4
    0xF0, 0x80, 0xF0, 0x10, 0xF0, #5
    0xF0, 0x80, 0xF0, 0x90, 0xF0, #6
    0xF0, 0x10, 0x20, 0x40, 0x40, #7
    0xF0, 0x90, 0xF0, 0x90, 0xF0, #8
    0xF0, 0x90, 0xF0, 0x10, 0xF0, #9
    0xF0, 0x90, 0xF0, 0x90, 0x90, #A
    0xE0, 0x90, 0xE0, 0x90, 0xE0, #B
    0xF0, 0x80, 0x80, 0x80, 0xF0, #C
    0xE0, 0x90, 0x90, 0x90, 0xE0, #D
    0xF0, 0x80, 0xF0, 0x80, 0xF0, #E
    0xF0, 0x80, 0xF0, 0x80, 0x80, #F
]


class Memory:
    def __init__(self, game, memory=4096):
        self.data = bytearray(memory)
        self.game = game
        self.default_fontset = default_fontset
        self.opcode_path = str(Path(__file__).resolve().parent.parent / "test_roms" / str(self.game))

    def load_rom(self):
        with open(self.opcode_path, "rb") as f: # open reading as binary (raw machine code)
            rom = f.read()
            self.data[0x200:0x200 + len(rom)] = rom
    
    def load_fontset(self):
        for i, byte in enumerate(self.default_fontset):
            self.data[i] = byte

    def dump(self, do_print: bool = False): # to verify memory was loaded / check its current state
        rows = []
        width = 16
        for i in range(0, len(self.data), width):
            chunk = self.data[i:i + width]
            hex_bytes = " ".join(f"{byte:02X}" for byte in chunk)
            rows.append(f"{i:04X}: {hex_bytes}")
        if do_print:
            print("\n".join(rows))
        else:
            return "\n".join(rows)
        



