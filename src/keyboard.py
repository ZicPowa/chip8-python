import pygame
import state

keyset = {
    '1': 0x1,
    '2': 0x2,
    '3': 0x3,
    '4': 0xC,
    'q': 0x4,
    'w': 0x5,
    'e': 0x6,
    'r': 0xD,
    'a': 0x7,
    's': 0x8,
    'd': 0x9,
    'f': 0xE,
    'z': 0xA,
    'x': 0x0,
    'c': 0xB,
    'v': 0xF,
}

class Keyboard:
    def __init__(self):
        self.keyset = keyset
        self.pressed_keys = set()
    def check_key_down(self, event):
        if event.type not in (pygame.KEYDOWN, pygame.KEYUP):
            return
        key_name = pygame.key.name(event.key)
        if key_name == "escape":
            state.game_running = False
            return
        if key_name not in self.keyset:
            return
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(self.keyset[key_name])
        else:
            self.pressed_keys.discard(self.keyset[key_name])


    def get_pressed_key(self):
        if self.pressed_keys:
            return next(iter(self.pressed_keys))
        return None