#!/usr/bin/env python

"""\
Handle incoming calls by replying with an SMS

"""

#from __future__ import print_function

import time, logging

PORT = '/dev/ttyACM99'
BAUDRATE = 9600
PIN = None # SIM card PIN (if any)

from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import InterruptedException, PinRequiredError, IncorrectPinError, TimeoutException

def handleIncomingCall(call):
    alreadyResponded=False
    if call.ringCount == 1:
        print 'Incoming call from: {0}'.format(call.number)
    elif not (call.number is None):
        alreadyResponded=True
        try:
           sms = modem.sendSms(call.number, 'Text')
        except TimeoutException:
           print 'Failed to send message: the send operation timed out'
        else:
           if sms.report:
                print 'Message sent{0}'.format(' and delivered OK.' if sms.status == SentSms.DELIVERED else ', but delivery failed.')
           else:
                print 'Message sent.'
    else:
        print ' Call from {0} is still ringing...'.format(call.number)
    
def main():
    print 'Initializing modem...'
    #logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    global modem
    modem = GsmModem(PORT, BAUDRATE, incomingCallCallbackFunc=handleIncomingCall)
    while True:
      modem.connect(PIN)
      print 'Waiting for incoming calls...'
      try:    
	modem.rxThread.join(10) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
      finally:
	modem.close()
	print "Reopening modem..."

if __name__ == '__main__':
    main()
