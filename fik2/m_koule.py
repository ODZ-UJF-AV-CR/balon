#!/usr/bin/python
#
# Non-threaded NB poller
# 

import time
import datetime
import logging
import serial
import math
import sys
import threading

port = '/dev/ttyUSB2'

baud = 9600


def handle_data(data):
  sys.stderr.write(data + "\n")
  datafname = "/data/balon/data_koule.csv"
  with open(datafname, "a") as nbf:
    nbf.write(data)
  nbf.close()

def read_from_port(ser):
  connected = False
  while not connected:
    #serin = ser.read()
    connected = True

    while True:
      reading = ser.readline().rstrip()
      if (len(reading) > 0):
        handle_data(str(time.time()) + ',' + reading + '\n')

ser = serial.Serial(port, baud, timeout=5)
read_from_port(ser)

#serial = serial.Serial(port, baud, timeout=5)
#thread = threading.Thread(target=read_from_port, args=(serial_port,))
#thread.start()

