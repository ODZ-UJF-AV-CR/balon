#!/usr/bin/env python
import sys
#from http import client
import httplib
import json
import datetime
#import pynmea2
#import urllib
#import urllib.request
from pymavlink import mavutil
import time
import crc16
import serial
from base64 import b64encode
from hashlib import sha256
from datetime import datetime
import Queue
from threading import Thread

callsign = "LetFik5"

if len(sys.argv) < 3: # Terminate program, if run without defining port as an argument
    print "Usage: python %s [recv port] [receiver callsign]" % sys.argv[0]
    sys.exit()

###################################################################


def make_sentence(sentence, checksum_bool): # Function which takes NMEA sentence as an argument
                                            # and returns sentence suitable for uploading to DB

    # Creates new sentence in format configured on Habitat's webpage
    new_sentence = callsign + ",{},{},{},{:0.0f},{}".format(sentence['timestamp'], sentence['lat'], sentence['lon'], sentence['altitude'], sentence['num_sats'])
    new_sentence = "$$" + new_sentence + "*" + str(checksum(new_sentence)) + '\n'
    #new_sentence = '$$LetFik5,123,13:16:24,51.123,0.123,11000*ABCD'
    print(new_sentence)
    return(new_sentence)


def make_data(sentence, callsign): # Creates data in format suitable for upload to DB
    date = datetime.utcnow().isoformat("T") + "Z"
    sentence = b64encode(sentence) 
    data = {
        "type": "payload_telemetry",
        "data": {
            "_raw": sentence
            },
        "receivers": {
            sys.argv[2]: {
                "time_created": get_date(True),
                "time_uploaded": get_date(True),
                # "time_created": date,
                # "time_uploaded": date
                },
            },
    }
    return data


def checksum(sentence): # Returns crc16-citt checksum of ASCII string
    crc = crc16.crc16xmodem(sentence.encode(), 0xffff)
    return ('{:04X}'.format(crc))


def get_date(format_bool):
    if format_bool == True:
        return (datetime.utcnow().isoformat("T") + "Z")
    else:
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


timestamp = '00:01:01'
latitude = 0.00
longtitude = 0.00
altitude = -1
timestamp = datetime.utcnow().strftime("%H:%M:%S")
num_sats = -1
date = get_date(False)

q = Queue.Queue(10)
#mav = mavutil.mavlink_connection(sys.argv[1], baud=9600, source_system=255)
mav = None

def get_mavlink(q, mav):
    mav = mavutil.mavlink_connection(sys.argv[1], baud=57600, source_system=255)

    while True:
        try:
            data = mav.recv_match(blocking=True)
            #print(data)
            data = data.to_dict()
            if data['mavpackettype'] == "GPS_RAW_INT":
                print(data)
                q.put({
                    'lat': data['lat']/10e6,
                    'lon': data['lon']/10e6,
                    'alt': data['alt']/10e2,
                    'time': data['time_usec'],
                    'source': 'mavlink',
                    'num_sats': data['satellites_visible']
                })
                q.task_done()
        except Exception as e:
            print("task error:", e)

worker = Thread(target=get_mavlink, args=(q, mav))
worker.setDaemon(True)
worker.start()

virtual = True;

try:
    while True: # Infinite loop waiting for data from configured serial port
        try:
            
            if not virtual:
                data = q.get(True)
                param = {
                    #'timestamp': datetime.fromtimestamp(data['time']).strftime("%H:%M:%S"),
                    'timestamp': datetime.utcnow().strftime("%H:%M:%S"),
                    'lat': data['lat'],
                    'lon': data['lon'],
                    'altitude': data['alt'],
                    'num_sats': data.get('num_sats', -1),
                }

            else:
                param = {
                    #'timestamp': datetime.fromtimestamp(data['time']).strftime("%H:%M:%S"),
                    'timestamp': datetime.utcnow().strftime("%H:%M:%S"),
                    'lat': 50.12,
                    'lon': 14.5,
                    'altitude': 200,
                    'num_sats': 0,
                }


            sentence = make_sentence(param, True)

            print("Sending: " + sentence)    # Prints sentence uploading to DB to the terminal              
            
            for x in range(0,4):
                try:

                    addr = "/habitat/_design/payload_telemetry/_update/add_listener/%s" % sha256(b64encode(sentence.encode())).hexdigest()
                    body = json.dumps(make_data(sentence, callsign))
                    
                    c = httplib.HTTPConnection("habitat.habhub.org") # DB uploader
                    c.request(
                        "PUT",
                        addr,
                        body.encode(),  # BODY
                        {
                            "Content-Type": "application/json",
                            'Accept': "application/json"
                        }
                    )

                    response = c.getresponse() # Prints response from DB
                    #print(response.read())


                except Exception as e:
                    if x < 3:
                        print("No internet connection. Repeating upload... [" + str(x + 1) +"/3]") # In case of no internet connection repeats upload three times
                        print(e)
                    else:
                        print("Error! No internet connection - sentence not sent") # If after three tries is sentence not uploaded, create log entry and continue
                        index_raw += 1
                        index += 1
                
        except Exception as e: # Close safely in case of port disconnection
            print("Error:", e)
        #time.sleep(0.5)

except KeyboardInterrupt: # Close safely with "CTRL + C"
    print("_Program closed\n")

#printer.close()
#printer_raw.close()
#printer_candy.close()
