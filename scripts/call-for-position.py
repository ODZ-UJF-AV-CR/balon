#!/usr/bin/env python

"""\
Handle incoming calls by replying with an SMS

GPS parts reused from Dan Mandle http://dan.mandle.me September 2012, License: GPL 2.0 
"""

import time, logging
import os
from gps import *
#from time import *
import threading
import sys

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

gpsd = None #seting the global variable

PORT = '/dev/ttyACM99'
BAUDRATE = 9600
PIN = None # SIM card PIN (if any)

from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import InterruptedException, PinRequiredError, IncorrectPinError, TimeoutException

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    logging.debug('GPS thread started')
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

def handleIncomingCall(call):
    if call.ringCount == 1:
        logging.info('Incoming call from: {0}'.format(call.number))
    elif (call.ringCount == 3) and not (call.number is None):
        destination=call.number
        #call.hangup() # That's messy, let's not use it.
        try:
           # Get a GPS fix, prepare a string with it
           zerotime=time.clock()
           timetowait=10.0
           while (gpsd.fix.mode < 2) and (clock() - zerotime < timetowait):
              sleep(1) #set to whatever

           smstext= "{0} {1} alt:{2}m http://www.google.com/maps/place/{3},{4}".format(gpsd.utc, gpsd.fix.mode, gpsd.fix.altitude, gpsd.fix.latitude,gpsd.fix.longitude)
           sms = modem.sendSms(destination, smstext, waitForDeliveryReport=True)
        except TimeoutException:
           logging.warn('Failed to send message to {0}: the send operation timed out'.format(call.number))
        else:
           if sms.report:
                logging.info('Message sent{0}'.format(' and delivered OK.' if sms.status == SentSms.DELIVERED else ', but delivery failed.'))
           else:
                logging.info('Message sent.')
    else:
        logging.info('Call from {0} is ringing...'.format(call.number))
    
if __name__ == '__main__':
    print "Initializing GPS thread"
    gpsp = GpsPoller() # create the thread
    try:
      gpsp.start() # Start GPS poller thread
    
      logging.info('Initializing modem...')
      #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
      global modem
      modem = GsmModem(PORT, BAUDRATE, incomingCallCallbackFunc=handleIncomingCall)

      while True:
        modem.connect(PIN)
        logging.info('Waiting for incoming calls...')
        try:    
  	  modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
        finally:
	  modem.close()
	  logging.info("Modem closed.")

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
      logging.info("Killing GPS thread...")
      gpsp.running = False
      gpsp.join() # wait for the thread to finish what it's doing
      sys.exit(1)

