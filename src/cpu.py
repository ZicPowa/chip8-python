#src/cpu.py: fetch, decode, and execute opcodes from self.data,
#starting at 0x200.

class CPU:
    def __init__(self, memory):
        self.memory = memory
