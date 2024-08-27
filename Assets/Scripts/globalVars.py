from copy import copy
import sounds
import random
import pygame
import arcade

LAST_VIEW = None

LIFES = 3
TOTAL_LIFES = copy(LIFES)
APPEND_LIFES = 0

MUSIC: pygame.mixer.Sound = sounds.ambient[random.randint(0,2)]
MUSIC = MUSIC.play()
MUSIC.stop()

CW_INDEXS = []

HELPS = 0