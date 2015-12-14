#!/usr/bin/python

# Monitor script

# GPS part from code by Dan Mandle http://dan.mandle.me September 2012, License: GPL 2.0 

import time
import datetime
import sys
import logging 

import os
import threading

import pygame
import pygame.camera

#### Settings #####
data_dir="/data/balon/"
imagedir=data_dir+"img/"

# Webcam #
#video_devices=["/dev/video0","/dev/video1"]
video_devices=["/dev/video0"]
resolutionx=1280 # Max 1600
resolutiony=720 # Max 480
skipframes=50
beattime=10

###########################
def make_selfie():
 for video_device in video_devices:
  device_number = video_device[-1]
  if (not device_number.isdigit()):
    logging.error("Webcam device specification likely wrong, last char not a number: %s." % (video_device))
    continue
  else:
    device_number = int(device_number)
  
  logging.debug("Initializing camera {0} at {1} for {2}x{3} px JPEG every {4} s.".format(device_number,video_device,resolutionx,resolutiony,beattime))
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
  savefname=imagedir+('cam%d-' % (device_number))+time.strftime('%F_%T.jpg', time.gmtime())
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
    logging.debug("Thread initialization")
    threading.Thread.__init__(self)
    self.running = True
    self.name = 'WebCam'
    pygame.init()
    pygame.camera.init()

  def run(self):
    logging.debug("Thread starting")
    while self.running:
      zerotime=time.time()
      make_selfie()
      selfie_time=time.time()-zerotime
      if (selfie_time > beattime):
        logging.warn("Webcam image capture takes too long: {0} s, can not pad the beats to {1}.".format(selfie_time, beattime))
      else:
        tts = beattime-selfie_time
        ttstep = 0.1
        logging.debug("Capture took %.3f s. Next beat in %.3f s to pad to %.3f s." % (selfie_time, tts, beattime))
        while (tts > 1.0):
          time.sleep(ttstep)
          tts = tts - ttstep 
        time.sleep(tts)

    logging.debug("Thread exiting")

#### ensure_dir ####
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
          logging.info("Creating directory: {0}".format(d))
          os.makedirs(d)

#### main ####
if __name__ == '__main__':
  # Logging
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
    )
  try:
    # Webcam thread initialization and startup
    logging.info("Initializing image capture.")
    pygame.init()
    pygame.camera.init()
    webcam = WebCamCapture()
    webcam.start()
    while webcam.running:
      time.sleep(1)
  except (KeyboardInterrupt, SystemExit):
    logging.info("Exiting.")
    if webcam.running:
      webcam.running = False
      logging.info("Webcam thread asked to shut down.")

