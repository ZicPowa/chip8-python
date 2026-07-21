#src/cpu.py: fetch, decode, and execute opcodes from self.data,
#starting at 0x200.

class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.pc = 0x200 # program counter
    def load_opcode(self):
        # memory[pc] is high byte, memory[pc+1] is low byte
        self.opcode = (self.memory[self.pc] << 8 | self.memory[self.pc+1])
        self.pc += 2 # increment to read next instruction
        if self.pc >= len(self.memory) - 1: 
            raise IndexError("Program counter exceeded memory bounds")
    def decode(self):
        """
        function decode():
    first_nibble = (opcode AND 0xF000) SHIFT_RIGHT 12
    x            = (opcode AND 0x0F00) SHIFT_RIGHT 8
    y            = (opcode AND 0x00F0) SHIFT_RIGHT 4
    n            = (opcode AND 0x000F)          // already at the bottom, no shift
    nn           = (opcode AND 0x00FF)          // already at the bottom, no shift
    nnn          = (opcode AND 0x0FFF)          // already at the bottom, no shift

    store first_nibble, x, y, n, nn, nnn for execute to use
        """
        self.op = (self.opcode & 0xF000) >> 12
        self.x = (self.opcode & 0x0F00) >> 8
        self.y = (self.opcode & 0x00F0) >> 4
        self.n = (self.opcode & 0x000F)
        self.nn = (self.opcode & 0x00FF)
        self.nnn = (self.opcode & 0x0FFF)

    def dispatch(self):
        pass

