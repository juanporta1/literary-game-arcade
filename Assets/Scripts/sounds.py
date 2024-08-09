from pygame.mixer import Sound
import pygame.mixer

pygame.mixer.init()

defeat = Sound("Sounds/defeat.mp3")
walk = Sound("Sounds/walk.mp3")

write1 = Sound("Sounds/write1.mp3")
write2 = Sound("Sounds/write2.mp3")
write3 = Sound("Sounds/write3.mp3")
write4 = Sound("Sounds/write4.mp3")

writes = [write1, write2, write3,write4]