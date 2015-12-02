#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0 

import os
from gps import *
from time import *
import time
import threading
import sys

gpsd = None #seting the global variable

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    zerotime=time.time()
    timetowait=30.0
    while (not 'T' in  gpsd.utc and gpsd.fix.mode < 2) and (time.time() - zerotime < timetowait):
      time.sleep(1) #set to whatever

    #print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
    #print 'mode        ' , gpsd.fix.mode
    #print 
    s=gpsd.utc
    if ('T' in s) and ('.' in s):
      datetime=s[:s.find('T')]+' '+s[s.find('T')+1:s.find('.')]
      print datetime
    else:
      print s
    
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    sys.exit(1)

