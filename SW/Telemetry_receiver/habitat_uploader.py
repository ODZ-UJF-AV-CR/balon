#!/usr/bin/env python
import sys
import httplib
import json
import pynmea2
import crc16
import serial
from base64 import b64encode
from hashlib import sha256
from datetime import datetime
### testovaci knihovna
import random

def make_sentence (sentence):
    parsed = pynmea2.parse(sentence, False)
    ### iterace vysky letu pro testovani (aby habitat databaze nehazela error kvuli identickym zpravam)
    parsed.altitude = str(round(random.uniform(40000,1),1))
    ###
    if parsed.lat_dir == 'S':
        parsed.lat = str(float(parsed.lat) * (-1))
    if parsed.lon_dir == 'W':
        parsed.lon = str(float(parsed.lon) * (-1))
    new_sentence = "ODZUJF,%s,%s,%s,%s" % (parsed.timestamp, parsed.lat, parsed.lon, parsed.altitude)
    new_sentence = "$$" + new_sentence + "*" + str(checksum(new_sentence)) + '\n'
    return(new_sentence)

def checksum(sentence):
    crc = str(hex(crc16.crc16xmodem(sentence, 0xffff)))
    crc_part = crc[2:6]
    return(crc_part.upper())


#if len(sys.argv) < 2:
 #   print "Usage: python %s <sentence> [recv callsign]" % sys.argv[0]
  #  sys.exit()

#pozdeji pro vstup ze seriove linky
#ser = serial.Serial('/dev/ttyACM0', timeout=3)
#data = ser.readline()

data = "$GPGGA,152225.00,5008.11103,S,01425.81157,W,2,07,1.25,317.1,M,44.3,M,,0000"

sentence = make_sentence(data)

print(sentence)


sentence = b64encode(sentence)

callsign = "ODZUJF" #if len(sys.argv) > 2 else "HABTOOLS"

date = datetime.utcnow().isoformat("T") + "Z"

data = {
    "type": "payload_telemetry",
    "data": {
        "_raw": sentence
        },
    "receivers": {
        callsign: {
            "time_created": date,
            "time_uploaded": date,
            },
        },
}

c = httplib.HTTPConnection("habitat.habhub.org")
c.request(
    "PUT",
    "/habitat/_design/payload_telemetry/_update/add_listener/%s" % sha256(sentence).hexdigest(),
    json.dumps(data),  # BODY
    {"Content-Type": "application/json"}  # HEADERS
    )

response = c.getresponse()

print response.status, response.reason
print response.read()
