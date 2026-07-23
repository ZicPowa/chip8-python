import pygame
class Keyboard:
    def __init__(self, keyset=['1', '2', '3', '4', 'q', 'w', 'e', 'r', 'a', 's', 'd', 'f', 'z', 'x', 'c', 'v']):
        self.keyset = keyset
    def check_key_down(self, event):
        
