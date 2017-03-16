#!/usr/bin/python

import time
import os
import sys
import pygame
import pygame.camera
import logging
import threading
from pygame.locals import *

pygame.init()
pygame.camera.init()

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
imagedir="img/"
video_device="/dev/video0"
resolutionx=1600
resolutiony=1200
skipframes=10

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
          logging.info("Creating directory: {0}".format(d))
          os.makedirs(d)

####################################################################
def make_selfie():
  logging.debug("Initializing camera at {0}".format(video_device))
  try:
    cam = pygame.camera.Camera(video_device,(resolutionx,resolutiony))
    cam.start()

  except SystemError as e:
    logging.error(e)
    return(1)

  # Wait for initialization
  while (not cam.query_image()):
    time.sleep(0.1)

  # Skip required number of frames
  if (skipframes > 0):
    logging.debug("Waiting for image stabilization - skipping {0} frames.".format(skipframes))
    for i in range(skipframes):
      try:
        img = cam.get_image()
      except pygame.error:
        logging.error("Error during frame capture: {0}".format(sys.exc_info()[0]))
        return(2)

  # Construct file name
  savefname=time.strftime(imagedir+'%F_%T.jpg', time.gmtime())
  logging.info("Capturing {0}x{1} frame to {2}.".format(resolutionx,resolutiony,savefname))
  try:
    ensure_dir(savefname)
    img = cam.get_image()
    pygame.image.save(img, savefname)
    cam.stop()
  except pygame.error as e:
    logging.error("Capture failed: {0}".format(e))

####################################################################
class WebCamCapture(threading.Thread):
  def __init__(self):
    logging.debug("WebCam thread initialization")
    threading.Thread.__init__(self)
    self.running = True
    self.looptime = 30
    self.name = 'WebCam'
  
  def run(self):
    logging.debug("Thread starting")
    while webcam.running:
      zerotime=time.time()
      make_selfie()
      selfie_time=time.time()-zerotime
      if (selfie_time > self.looptime):
        logging.warn("Webcam image capture takes too long: {0} s, can not pad the beats to {1}.".format(selfie_time, self.looptime))
      else:
        logging.debug("Capture took {0} s. Next beat in {1} s to pad to {2} s.".format(selfie_time, self.looptime-selfie_time, self.looptime))
        time.sleep(self.looptime-selfie_time)

    logging.debug("Thread exiting")

####################################################################

logging.info("Initializing image capture.")
webcam = WebCamCapture()
webcam.looptime = 10
webcam.start()
try:
  time.sleep(30)
except KeyboardInterrupt,SystemExit:
  logging.warn("Terminating run on request, wait.")
  
webcam.running = False
webcam.join()
logging.info("End.")

