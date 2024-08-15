from pygame.mixer import Sound
import pygame.mixer

pygame.mixer.init()

defeat = Sound("Sounds/defeat.mp3")


write1 = Sound("Sounds/write1.mp3")
write2 = Sound("Sounds/write2.mp3")
write3 = Sound("Sounds/write3.mp3")
write4 = Sound("Sounds/write4.mp3")

writes = [write1, write2, write3,write4]

footstep1 = Sound("Sounds/footstep1.mp3")
footstep2 = Sound("Sounds/footstep2.mp3")
footstep3 = Sound("Sounds/footstep3.mp3")
footstep1.set_volume(.5)
footstep2.set_volume(.5)
footstep3.set_volume(.5)
footsteps = [footstep1, footstep2, footstep3]

ambient:Sound = []
for i in range(1,4):
    ambient.append(Sound(f"Sounds/ambient{i}.mp3"))
    
mechanism = Sound("Sounds/mechanism.mp3")

getlife1 = Sound("Sounds/getlife1.mp3")

lostlife = Sound("Sounds/lostlife.mp3")

fall1 = Sound("Sounds/fall1.mp3")

floorbreakings: list[Sound] = []

for i in range(1,5):
    sound = Sound(f"Sounds/floorbreaking{i}.mp3")
    floorbreakings.append(sound)
    