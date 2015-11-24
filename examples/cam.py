#!/usr/bin/python

import time
import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera("/dev/video0",(1600,1200))
cam.start()

time.sleep(0.5)
img = cam.get_image()
img = cam.get_image()
img = cam.get_image()
img = cam.get_image()
img = cam.get_image()
pygame.image.save(img, "photo.bmp")
pygame.camera.quit()

