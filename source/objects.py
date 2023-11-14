import pygame
from source.SETTINGS import *

class Card(pygame.Rect):
    def __init__(self,card_name, value, img, x = 0,y = 0):
        super().__init__(x, y, CARD_GAME_WIDTH, CARD_GAME_HEIGHT)
        self.up = False
        self.lock = False
        self.card_name = card_name
        self.value = value
        self.image = img