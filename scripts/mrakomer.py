#!/usr/bin/python
#
# Non-threaded NB poller
# 

import m_settings as g
import time
import datetime
import logging
import serial
import math
import threading

port = '/dev/ttyUSB1'

baud = 9600

serial_port = serial.Serial(port, baud, timeout=5)

def handle_data(data):
  print(data)
  datafname = "data_koule.csv"
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
        handle_data(str(time.time()) + ' ' + reading + '\n')

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()

