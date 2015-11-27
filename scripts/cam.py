#!/usr/bin/python

import time
import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera("/dev/video0",(1600,1200))
cam.start()

# Wait for initialization
time.sleep(0.5)

# Skip required number of frames
nskip=10
for i in range(nskip):
 img = cam.get_image()

pygame.image.save(img, "photo.jpg")
pygame.camera.quit()

