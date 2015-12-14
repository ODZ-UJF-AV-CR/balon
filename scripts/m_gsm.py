#!/usr/bin/python

# Monitor script

# GPS part from code by Dan Mandle http://dan.mandle.me September 2012, License: GPL 2.0 

import time
import datetime
import sys
import logging 
import re
import os
import threading

import m_gps

## Modem
from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import InterruptedException, PinRequiredError, IncorrectPinError, TimeoutException
###

modem=None

# GSM module #
default_destination = "+420777642401"
PORT = '/dev/ttyACM99'
BAUDRATE = 9600 # Higher baud rates than 9600 lead to errors
PIN = None # SIM card PIN (if any)

#### Send position in a SMS ########################################
def send_position_via_sms(destination):
    logging.info("Will send position via SMS to: {0}.".format(destination))
    # Get current time

    try:
       # Get a GPS fix, prepare a string with it
       if (m_gps.lv('GPS_Fix') < 3):
         timestring = time.strftime('%T', time.gmtime())
         smstext = "{0} GSM: {1}".format(timestring, gsmpart.cellInfo) 
       else:
         timestring = time.strftime('%T', time.gmtime())
         smstext = "{0} alt{1} http://www.google.com/maps/place/{2},{3}".format(timestring, m_gps.lv("GPS_Alt"), m_gps.lv("GPS_Lat"), m_gps.lv("GPS_Lon"))

       #if ('Bat_Temp' in sensors) and ('Bat_Charge' in sensors):
       #  smstext = smstext + (" BT{0} BCH{1} ".format(sv('Bat_Temp'), sv('Bat_Charge')))
       #else:
       #  smstext = smstext + " NoBatInfo"

       sms = modem.sendSms(destination, smstext, waitForDeliveryReport=True)
    except TimeoutException:
       logging.warn('Failed to send message to {0}: the send operation timed out'.format(call.number))
    else:
       if sms.report:
            logging.info('Message sent{0}'.format(' and delivered OK.' if sms.status == SentSms.DELIVERED else ', but delivery failed.'))
       else:
            logging.info('Message sent.')


#### Incoming call handler #########################################
def handleIncomingCall(call):
    if call.ringCount == 1:
        logging.info('New incoming call, waiting for CLIP.'.format(call.number))
    elif call.ringCount <= 3 and not (call.number is None):
        logging.info('Got CLIP, Will send position to {0}.'.format(call.number))
        destination=call.number
        call.hangup()
        send_position_via_sms(destination)
    elif call.ringCount > 3:
        call.hangup()
        send_position_via_sms(default_destination)
    else:
        logging.info('Call is ringing and we still have no CLIP.')
         
# Modem GPIO reset handler
def writepins(pin_value):
    pin = open("/sys/class/gpio/gpio204/value","w")
    pin.write(pin_value)
    pin.close()

def exportpins():
    logging.debug("Exporting GPIO pin")
    GPIO_EXPORT_PATH=os.path.normpath('/sys/class/gpio/export')
    GPIO_MODE_PATH= os.path.normpath('/sys/class/gpio/gpio204/direction')
    if (os.path.isdir('/sys/class/gpio/gpio204')):
      logging.debug("/sys/class/gpio/gpio204 directory already exists, export not needed")
    else:
      try:
        file = open(GPIO_EXPORT_PATH, 'w')
        file.write("204")          ## export the pin to the usermode
        file.close()

        file = open(GPIO_MODE_PATH, 'r+')
        file.write("out")          ## make the pin as output
        file.close()
      except:
        logging.error("Trouble exporting GPIO pin for modem reset.")

class ModemHandler(threading.Thread):
  # +CGED: MCC:230, MNC:  3, LAC:878c, CI:2a95,
  CGED_REGEX = re.compile(r'^\+CGED:\s*MCC:([^,]+),\s*MNC:\s*([^,]+),\s*LAC:\s*([^,]+),\s*CI:\s*([^,]+),.*')
  def __init__(self):
    logging.info("Starting Modem handler thread")
    threading.Thread.__init__(self)
    global modem
    self.running = True #setting the thread running to true
    self.name = "Modem"
    self.networkName = "none"
    self.signalStrength = -1
    self.cellInfo = "none"
 
  def modemPowerCycle(self):
    # Should reset the modem using hardware pin
    exportpins()
    writepins('0')
    time.sleep(2)
    writepins('1') 

  def get_status_string(self):
    return("GSM: %d %s Cell: %s " % (self.signalStrength,self.networkName, self.cellInfo))

  def get_record(self):
    return("%d\t%s\t" % (self.signalStrength, self.cellInfo))
 
  def get_header(self):
    return('GSM_signal\tGSM_CellInfo\t')

  def run(self):
    # Initialize the GPIO interface
    #exportpins()
    #writepins('1')
    
    logging.info("Modem thread running")
    global modem
    rxListenLength = 5
    init_count = 0
    
    while self.running and init_count > -1:
      try:
        init_count = init_count + 1
        modem = GsmModem(PORT, BAUDRATE, incomingCallCallbackFunc=handleIncomingCall)
        logging.info("Initializing modem, try {0}.".format(init_count))
        modem.connect(PIN)
        init_count = -1
      except (OSError, TimeoutException):
        # OSError means pppd is likely running
        logging.error("Failed to initialize the GSM module.")
        try:
          modem.close()
        except AttributeError:
          True 
        time.sleep(5)
        #self.modemPowerCycle()

    logging.info('Waiting for incoming calls...')
    while self.running:
      try:
        #waitForNetworkCoverage()
        self.signalStrength = modem.signalStrength
        self.networkName = modem.networkName
        #modem.write("AT+CFUN=0")
        serving_cell=self.CGED_REGEX.match(modem.write("AT+CGED=3")[0])
        if serving_cell:
          mcc=serving_cell.group(1)
          mnc=serving_cell.group(2)
          lac=serving_cell.group(3)
          ci=serving_cell.group(4)
          self.cellInfo="{0}/{1}/{2}/{3}".format(mcc, mnc, lac, ci)

        # Comms are handled elsewhere so we could eventually just sleep, waiting
        #time.sleep(rxListenLength)
        modem.rxThread.join(rxListenLength) 
      except (InterruptedException, PinRequiredError, IncorrectPinError, TimeoutException):
        logging.error("rxThread died: {0}".format(sys.exc_info()[0]))

    modem.close()
    logging.info("Modem closed.")

#### main ####
if __name__ == '__main__':
  # Logging
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
    )
  try:
    # GPS thread initialization and startup
    gpsp = m_gps.GpsPoller() # create the thread
    gpsp.start() # start it up

    # GSM call/sms handler
    logging.info("Initializing GSM support.")
    gsmpart = ModemHandler()
    gsmpart.start()
    while gsmpart.running:
      # GSM module data
      logging.info(gsmpart.get_status_string())
      time.sleep(10)
      send_position_via_sms(default_destination)
  except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting.")
    if gsmpart.running:
      gsmpart.running = False
      logging.info("GSM part asked to shut down.")
    if gpsp.running:
      logging.info("GPS part asked to shut down.")
      gpsp.running = False
    sys.exit(0)

