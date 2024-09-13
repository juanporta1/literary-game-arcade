from copy import copy
import sounds
import random
import pygame
import arcade

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
ACTUAL_WIDTH = 1280
ACTUAL_HEIGHT = 720

LAST_VIEW = None

LIFES = 3
TOTAL_LIFES = copy(LIFES)
APPEND_LIFES = 0

MUSIC: pygame.mixer.Sound = sounds.ambient[random.randint(0,2)]
MUSIC = MUSIC.play()
MUSIC.stop()

CW_INDEXS = []
HM_INDEXS = []
HELPS = 0