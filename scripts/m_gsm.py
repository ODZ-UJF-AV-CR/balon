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
import subprocess

import m_gps
import m_i2c

import m_settings as g

## Modem
from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import InterruptedException, PinRequiredError, IncorrectPinError, TimeoutException, CommandError
###

modem=None
ppp_requested = False
beat = 0

sms_queue = []
#'position']

# GSM module #
default_destination = g.default_destination
PORT = '/dev/ttyACM99'
BAUDRATE = 9600 # Higher baud rates than 9600 lead to errors
PIN = None # SIM card PIN (if any)

data = {}

# Get sensor value or -1 if not available
def dv(sname):
  if sname in data:
    return(data[sname])
  else:
    return(-1)

#### Send position in a SMS ########################################
def send_position_via_sms(destination):
    global modem
    logging.info("Will send position via SMS to: {0}.".format(destination))
    # Get current time

    try:
       # Get a GPS fix, prepare a string with it
       if (m_gps.lv('GPS_Fix') < 3):
         timestring = time.strftime('%T', time.gmtime())
         smstext = "{0} GSM: {1}".format(timestring, data['cellInfo']) 
       else:
         timestring = time.strftime('%T', time.gmtime())
         #smstext = "{0} alt{1} http://www.google.com/maps/place/{2},{3} S{4}C{5}".format(timestring, m_gps.lv("GPS_Alt"), m_gps.lv("GPS_Lat"), m_gps.lv("GPS_Lon"), dv('signalStrength'), dv('cellInfo'))
         smstext = "{0} h{1} http://www.google.com/maps/place/{2},{3} Spd{4} Tr{5} Cl{6} {7}ID{8}".format(timestring, m_gps.lv("GPS_Alt"), m_gps.lv("GPS_Lat"), m_gps.lv("GPS_Lon"), m_gps.lv('GPS_Speed'), m_gps.lv('GPS_Track'), m_gps.dv('GPS_AvgClimb'), dv('signalStrength'), dv('cellInfo'))

       if len(smstext) > 130:
           smstext = "Alt{1} Lat{2} Lon{3} v{4} Tr{5} Cl{6} {7}ID{8}".format(m_gps.lv("GPS_Alt"), m_gps.lv("GPS_Lat"), m_gps.lv("GPS_Lon"), m_gps.lv('GPS_Speed'), m_gps.lv('GPS_Track'), m_gps.lv('GPS_AvgClimb'), dv('signalStrength'), dv('cellInfo'))

       if ('Bat_Temp' in m_i2c.data) and ('Bat_Charge' in m_i2c.data):
         smstext = smstext + (" BT{0} BCH{1} ".format(m_i2c.dv('Bat_Temp'), m_i2c.dv('Bat_Charge')))
       else:
         smstext = smstext + " NoBatInfo"

       logging.warn('SMS text length {0}'.format(len(smstext)))
       logging.warn('SMS: {0}'.format(smstext))

       sms = modem.sendSms(destination, smstext, waitForDeliveryReport=False)
    except TimeoutException:
       logging.warn('Failed to send message to {0}: the send operation timed out'.format(destination))
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

def handleSms(sms):
  global ppp_requested
  global sms_queue
  logging.info('SMS From {0} at {1}:{2}'.format(sms.number, sms.time, sms.text))
  if sms.text.lower() == 'pos':
    logging.info('SMS: Position request')
    sms_queue.append('position')
  elif sms.text.lower() == 'ppp':
    logging.info('SMS: GSM uplink requested')
    sms_queue.append('Activating PPP uplink')
    ppp_requested = True
  else:
    logging.info('SMS: Command not understood')
    
def get_header():
  return('GSM_signal\tGSM_CellInfo\t')

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
    self.do_shutdown = False
 
  def modemPowerCycle(self):
    # Should reset the modem using hardware pin
    exportpins()
    writepins('0')
    time.sleep(2)
    writepins('1') 

  def shutdown(self):
    self.do_shutdown = True

  def get_status_string(self):
    if self.signalStrength < 100:
      return("GSM: %d @ %s Cell: %s " % (self.signalStrength,self.networkName, self.cellInfo))
    else:
      return("GSM: PPP @ %s Cell: %s " % (self.networkName, self.cellInfo))

  def get_record(self):
    return("%d\t%s\t" % (self.signalStrength, self.cellInfo))
 

  def run(self):
    # Initialize the GPIO interface
    #exportpins()
    #writepins('1')
    
    logging.info("Modem thread running.")

    global modem
    global ppp_requested
    global sms_queue
    global beat

    rxListenLength = 10
    init_count = 0
    
    while self.running:
      beat += 1
      while self.running and not ppp_requested and init_count > -1:
        try:
          init_count = init_count + 1
          modem = GsmModem(PORT, BAUDRATE, incomingCallCallbackFunc=handleIncomingCall, smsReceivedCallbackFunc=handleSms)
          logging.info("Initializing modem, try {0}.".format(init_count))
          modem.connect(PIN)
          modem.write('AT+CFUN=1') 
          init_count = -1
        except (OSError, TimeoutException,CommandError):
          # OSError means pppd is likely running
          logging.error("Failed to initialize the GSM module.")
          try:
            modem.close()
          except AttributeError:
            True 
          time.sleep(5)
          #self.modemPowerCycle()

      logging.info('Waiting for incoming calls...')
      while self.running and not ppp_requested and init_count < 0:
        try:
          #waitForNetworkCoverage()
          self.signalStrength = modem.signalStrength
          self.networkName = modem.networkName
          data['signalStrength'] = self.signalStrength
          data['networkName'] = self.networkName
          #modem.write("AT+CFUN=1")
          serving_cell=self.CGED_REGEX.match(modem.write("AT+CGED=3")[0])
          if serving_cell:
            mcc=serving_cell.group(1)
            mnc=serving_cell.group(2)
            lac=serving_cell.group(3)
            ci=serving_cell.group(4)
            self.cellInfo="{0}/{1}/{2}/{3}".format(mcc, mnc, lac, ci)
            data['cellInfo'] = self.cellInfo

          # Comms are handled elsewhere so we could eventually just sleep, waiting
          #time.sleep(rxListenLength)
          if (self.signalStrength > 5):
            sent_position = 0
            while (len(sms_queue) > 0):
              text=sms_queue.pop()
              if (text == 'position') and sent_position:
                logging.info('Not resending position in the same interval')
              elif (text == 'position'):
                send_position_via_sms(default_destination)  
                sent_position = 1
              else:
                try:
                  modem.sendSms(default_destination, text, waitForDeliveryReport=False)
                except (CommandError, TimeoutException):
                  sms_queue.append(text)
          else:
            logging.info('Waiting for better network coverage')

          modem.rxThread.join(rxListenLength) 
          
          if self.do_shutdown:
            logging.warn('Disabling radio RX/TX.')
            modem.write('AT+CFUN=0') 
            self.running = False
            modem.close()

        except (CommandError, InterruptedException, PinRequiredError, IncorrectPinError, TimeoutException):
          logging.error("rxThread died: {0}".format(sys.exc_info()[0]))
          modem.close()
          time.sleep(5)
          init_count = 0

      # If PPP was requested, now it's the time
      if self.running and ppp_requested and self.signalStrength > 5 and init_count < 0:
        try:
          self.signalStrength = 101
          logging.info('Launching PPP session.') 
          while (len(sms_queue) > 0):
            logging.info('==== Sending PPP activation SMS =====')
            text=sms_queue.pop()
            try:
              modem.sendSms(default_destination, text, waitForDeliveryReport=False)
              time.sleep(1)
            except (CommandError, TimeoutException):
              sms_queue.append(text)
          #waitForNetworkCoverage()
          modem.close()
          logging.info("Modem interface closed.")
          rc = subprocess.check_output(['/usr/bin/timeout','360','/usr/bin/pon'], stderr=subprocess.STDOUT)
          logging.info('PPP ended: %s' % s)
        except subprocess.CalledProcessError as e:
          logging.info('PPP ended: %s' % e)
        sms_queue.append('PPP connection terminated')
        ppp_requested = False
        init_count = 0
      #end of if
    #end of while

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
      #i2c = m_i2c.get_i2c_data()
      time.sleep(10)
      logging.info(gsmpart.get_status_string())
      time.sleep(10)
      logging.info(gsmpart.get_status_string())
      time.sleep(10)
      gsmpart.shutdown()
      while gsmpart.isAlive():
        print "waiting for modem shutdown"
        time.sleep(1)
      print "Modem radio disabled and modem is down."
      time.sleep(10)
      
      gsmpart = ModemHandler()
      gsmpart.start()

    print "GSM part finished."
    raise(SystemExit)

#      time.sleep(10)
#      ppp_requested = True
#      time.sleep(600)
      #send_position_via_sms(default_destination)
  except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting.")
    if gsmpart.running:
      gsmpart.running = False
      logging.info("GSM part asked to shut down.")
    if gpsp.running:
      logging.info("GPS part asked to shut down.")
      gpsp.running = False
    sys.exit(0)

