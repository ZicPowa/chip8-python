#src/cpu.py: fetch, decode, and execute opcodes from self.data,
#starting at 0x200.

class CPU:
    def __init__(self, memory,display):
        self.memory = memory
        self.pc = 0x200 # program counter
        self.display = display
        self.stack = [0] * 16 # memory part of RAM
        self.registers = [0] * 16 # 'memory' within hardware CPU
        self.sp = 0 # stack pointer

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
        # written in order of cowgod technical reference - see readme
        if self.op == 0x0:
            if self.nn == 0x00e0: #cls clear display
                if self.display is not None:
                    self.display.clear()
                else:
                    raise RuntimeError("Display was not defined")

            elif self.nn == 0xee: # ret return from a subroutine
                self.sp -= 1
                self.pc = self.stack[self.sp]
        elif self.op == 0x1: # jump
            # no second level check required as jump is the only instruction with this op value
            self.pc = self.nnn
        elif self.op == 0x2: # call 
            self.sp += 1
            self.stack[self.sp] = self.pc

        elif self.op == 0x3: 
            # skip next instruction if vx = nn
            if self.registers[self.x] == self.nn:
                self.pc += 2

        elif self.op == 0x4: # skip next instruction if vx != kk
            if self.registers[self.x] != self.nn:
                self.pc += 2

        elif self.op == 0x5: # skip next instruction if vx = vy
            if self.registers[self.x] == self.registers[self.y]:
                self.pc += 2

        elif self.op == 0x6:
            self.registers[self.x] = self.nn

        elif self.op == 0x7:
            self.registers[self.x] += self.nn

        elif self.op == 0x8:
            if self.n == 0x0:
                self.registers[self.x] = self.registers[self.y]
            elif self.n == 0x1: # perform bitwise or
                self.registers[self.x] = self.registers[self.x] | self.registers[self.y]
            elif self.n == 0x2: # bitwise and
                self.registers[self.x] = self.registers[self.x] & self.registers[self.y]
            elif self.n == 0x3: #bitwise exor
                self.registers[self.x] = self.registers[self.x] ^ self.registers[self.y]
            elif self.n == 0x4:
                pass
                



