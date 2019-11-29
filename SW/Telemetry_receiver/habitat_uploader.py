#!/usr/bin/env python
import sys
import httplib
import json
import datetime

import time
import crc16

from base64 import b64encode
from hashlib import sha256
from datetime import datetime
import Queue
from threading import Thread


###################################################################

callsign = "LetFik5"
virtual = False;

###################################################################



def make_sentence(sentence, checksum_bool): # Function which takes NMEA sentence as an argument
                                            # and returns sentence suitable for uploading to DB

    # Creates new sentence in format configured on Habitat's webpage
    new_sentence = callsign + ",{},{},{},{},{},{},{}".format(sentence['timestamp'], sentence['lat'], sentence['lon'], sentence['altitude'], sentence['num_sats'], sentence['fix'], sentence['temperature'])
    new_sentence = "$$" + new_sentence + "*" + str(checksum(new_sentence)) + '\n'
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

if len(sys.argv) < 3: # Terminate program, if run without defining port as an argument
    print "Usage: python %s [recv port | lora] [receiver callsign]" % sys.argv[0]
    sys.exit()

date = get_date(False)
q = Queue.Queue(10)

def start_mavlink_rx(q):
    mav = mavutil.mavlink_connection(sys.argv[1], baud=57600, source_system=255)

    payload = {
            'lat': 0,
            'lon': 0,
            'alt': 0,
            'fix': 0,
            'time': 0,
            'source': 'mavlink',
            'num_sats': -1,
            'temp': 0

        }
    f=open("log_{}_mavlink.txt".format(callsign), "a+")

    while True:
        try:
            data = mav.recv_match(blocking=True)
            data = data.to_dict()
            if data['mavpackettype'] == "GPS_RAW_INT":
                payload['lat'] = data['lat']/10e6
                payload['lon'] = data['lon']/10e6
                payload['alt'] = data['alt']/10e2
                payload['time'] = data['time_usec']
                payload['num_sats'] = data['satellites_visible']
                f.write(json.dumps(data))

            # temperature
            #if data['mavpackettype'] == "":
            #    payload['temp'] = data['temperature']

            if data['mavpackettype'] in ['GPS_RAW_INT']:
                q.put(payload)
                q.task_done()

        except Exception as e:
            print("task error:", e)


def start_lora_rx(qu):
    app_id = "throwaway324s-test-network"
    access_key = "ttn-account-v2.zyaSIrWA1yJ_RdEgp7yDPhvTAH3-qEstQi6MMVrhzwo"

    f=open("log_{}_lora.txt".format(callsign), "a+")

    def uplink_callback(msg, client):
        try:
            print "New LoRa message:", msg.metadata.time, msg.counter, msg.payload_fields
            #qu.put(msg)
            fields = msg.payload_fields
            ts = iso8601.parse_date(msg.metadata.time)
            data = {
                "lat": fields.lat,
                "lon": fields.lon,
                "alt": float(fields.alt_m),
                "time": int((ts.utcnow()-datetime(1970,1,1)).total_seconds()*1000000),
                "source": "lora"
            }
            qu.put(data)
            q.task_done()

            f.write(json.dupms(data))

        except Exception as e:
            print("task error", e)

    handler = ttn.HandlerClient(app_id, access_key)

    # using mqtt client
    mqtt_client = handler.data()
    mqtt_client.set_uplink_callback(uplink_callback)
    mqtt_client.connect()


if sys.argv[1] == 'lora':
    import ttn
    import iso8601

    print("Starting LORA")
    reciever = start_lora_rx
else:
    import serial
    from pymavlink import mavutil

    reciever = start_mavlink_rx

worker = Thread(target=reciever, args=(q,))
worker.setDaemon(True)
worker.start()




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
                    'fix': data.get('fix', -1),
                    'temperature': data.get('temp', -999),
                }

            else:
                param = {
                    #'timestamp': datetime.fromtimestamp(data['time']).strftime("%H:%M:%S"),
                    'timestamp': datetime.utcnow().strftime("%H:%M:%S"),
                    'lat': 50.12,
                    'lon': 14.5,
                    'altitude': 200.34,
                    'num_sats': 0,
                    'fix': -1,
                    'temperature': 10,
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


except KeyboardInterrupt: # Close safely with "CTRL + C"
    print("_Program closed\n")
