#src/cpu.py: fetch, decode, and execute opcodes from self.data,
#starting at 0x200.
import random
import numpy
import pygame

pygame.mixer.init(frequency=44100, size=-16, channels=1)
def make_tone(frequency=440, duration=0.5, volume=0.5, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    t = numpy.linspace(0, duration, n_samples, endpoint=False)
    wave = numpy.sin(2 * numpy.pi * frequency * t)
    audio = (wave * volume * 32767).astype(numpy.int16)
    # have to make 2d because pygame returns an error needing 2d array
    stereo = numpy.column_stack([audio, audio])
    return pygame.sndarray.make_sound(stereo)

sound_tone = make_tone(440, 0.1)

class CPU:
    def __init__(self, memory, display, keyboard):
        self.memory = memory
        self.keyboard = keyboard
        self.pc = 0x200 # program counter
        self.display = display
        self.stack = [0] * 16 # memory part of RAM
        self.registers = [0] * 16 # 'memory' within hardware CPU
        self.sp = 0 # stack pointer
        self.i = 0 # index register holds a memory address - not a normal register like seen in self.registers of V0 to Vf
        self.dt = 0 # delay timer
        self.st = 0 # sound timer
        self.waiting_for_key = False
        self.waiting_register = 0
        self.tone_playing = False

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
            self.stack[self.sp] = self.pc
            self.sp += 1
            self.pc = self.nnn

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
            self.registers[self.x] = (self.registers[self.x] + self.nn) & 0xFF

        elif self.op == 0x8: # bulk of the arithmetic and bitwise logic
            if self.n == 0x0:
                self.registers[self.x] = self.registers[self.y]
            elif self.n == 0x1: # perform bitwise or
                self.registers[self.x] = self.registers[self.x] | self.registers[self.y]
            elif self.n == 0x2: # bitwise and
                self.registers[self.x] = self.registers[self.x] & self.registers[self.y]
            elif self.n == 0x3: #bitwise exor
                self.registers[self.x] = self.registers[self.x] ^ self.registers[self.y]
            elif self.n == 0x4:
                sum_value = self.registers[self.x] + self.registers[self.y]
                if sum_value > 0xFF:
                    self.registers[0xF] = 1
                else:
                    self.registers[0xF] = 0
                self.registers[self.x] = sum_value & 0xFF
            elif self.n == 0x5:
                vf = 1 if self.registers[self.x] >= self.registers[self.y] else 0
                self.registers[self.x] = (self.registers[self.x] - self.registers[self.y]) & 0xFF # locks to 8 bit
                self.registers[0xF] = vf
            elif self.n == 0x6:
                vf = self.registers[self.y] & 0x1
                self.registers[self.x] = self.registers[self.y] >> 1
                self.registers[0xF] = vf
            elif self.n == 0x7:
                vf = 1 if self.registers[self.y] >= self.registers[self.x] else 0
                self.registers[self.x] = (self.registers[self.y] - self.registers[self.x]) & 0xFF
                self.registers[0xF] = vf
            elif self.n == 0xE:
                vf = (self.registers[self.y] & 0x80) >> 7
                self.registers[self.x] = (self.registers[self.y] << 1) & 0xFF # mask to 8 bits
                self.registers[0xF] = vf

        elif self.op == 0x9:
            if self.registers[self.x] != self.registers[self.y]:
                self.pc += 2

        elif self.op == 0xA:
            self.i = self.nnn

        elif self.op == 0xB:
            self.pc = self.nnn + self.registers[0x0]

        elif self.op == 0xC:
            self.registers[self.x] = random.randint(0, 255) & self.nn

        elif self.op == 0xD: # DRAW
            x = self.registers[self.x] % 64 # wrap position to within the screen
            y = self.registers[self.y] % 32
            self.registers[0xF] = 0
            for row in range(self.n):
                sprite_byte = self.memory[self.i + row]
                pixel_y = y + row
                if pixel_y >= 32:
                    break # stop drawing if gone past bottom edge
                for col in range(8):
                    sprite_pixel = (sprite_byte >> (7 - col)) & 1
                    if sprite_pixel == 1:
                        pixel_x = x + col
                        if pixel_x >= 64:
                            continue # stop drawing if gone past right edge
                        index = pixel_y * 64 + pixel_x

                        if self.display.buffer[index] == 1:
                            self.registers[0xF] = 1 # collision

                        self.display.buffer[index] ^= 1

        elif self.op == 0xE:
            if self.nn == 0x9E:
                if self.registers[self.x] in self.keyboard.pressed_keys:
                    self.pc += 2
            elif self.nn == 0xA1:
                if self.registers[self.x] not in self.keyboard.pressed_keys:
                    self.pc += 2

        elif self.op == 0xF:
            if self.nn == 0x07:
                self.registers[self.x] = self.dt
            elif self.nn == 0x0A:
                self.waiting_for_key = True
                self.waiting_register = self.x
            elif self.nn == 0x15:
                self.dt = self.registers[self.x]
            elif self.nn == 0x18:
                self.st = self.registers[self.x]
            elif self.nn == 0x1E:
                self.i = (self.i + self.registers[self.x]) & 0xFFF
            elif self.nn == 0x29:
                self.i = self.registers[self.x] * 5
            elif self.nn == 0x33:
                self.memory[self.i] = self.registers[self.x] // 100
                self.memory[self.i+1] = (self.registers[self.x] // 10) % 10
                self.memory[self.i+2] = self.registers[self.x] % 10
            elif self.nn == 0x55:
                for register in range(self.x + 1):
                    self.memory[self.i + register] = self.registers[register]
                self.i += self.x + 1
            elif self.nn == 0x65: 
                for i in range(self.x + 1):
                    self.registers[i] = self.memory[self.i + i]
                self.i += self.x + 1
            # finally finished the opcodes :)

    def tick_timers(self):
        if self.dt > 0:
            self.dt -= 1
        if self.st > 0:
            self.st -= 1
            sound_tone.play(loops=-1)
            self.tone_playing = True
        else:
            if self.tone_playing:
                sound_tone.stop()
                self.tone_playing = False


    def cycle(self):

        if self.waiting_for_key:
            key = self.keyboard.get_pressed_key()
            if key is not None:
                self.registers[self.waiting_register] = key
                self.waiting_for_key = False
            return # stops from doing extra cpu work this cycle

        self.load_opcode()
        self.decode()
        self.dispatch()

                

