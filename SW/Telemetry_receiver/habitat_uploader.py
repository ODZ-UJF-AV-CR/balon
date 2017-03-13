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



def make_sentence(sentence, checksum_bool): # Function which takes NMEA sentence as an argument
                                            # and returns sentence suitable for uploading to DB
    try:
        try: 
            if checksum_bool == False:
                parsed = pynmea2.parse(sentence[:-4], checksum_bool)
            else:
                parsed = pynmea2.parse(sentence)
        except pynmea2.ChecksumError:
            return "wrong_checksum"
    except pynmea2.nmea.ParseError:
        return "parse_error"

    if parsed.lat_dir == 'S':
        parsed.lat = str(float(parsed.lat) * (-1))
    if parsed.lon_dir == 'W':
        parsed.lon = str(float(parsed.lon) * (-1))
    # Creates new sentence in format configured on Habitat's webpage
    new_sentence = "ODZUJF,%s,%s,%s,%s,%s" % (parsed.timestamp, parsed.lat, parsed.lon, parsed.altitude, parsed.num_sats)
    new_sentence = "$$" + new_sentence + "*" + str(checksum(new_sentence)) + '\n'
    return(new_sentence)

def checksum(sentence): # Returns crc16-citt checksum of ASCII string
    crc = crc16.crc16xmodem(sentence, 0xffff)
    return ('{:04X}'.format(crc))



if len(sys.argv) < 2: # Terminate program, if run without defining port as an argument
    print "Usage: python %s [recv port]" % sys.argv[0]
    sys.exit()

#### only for testing with simulated GPS, might need some changes
ser = serial.Serial(sys.argv[1], rtscts=True, dsrdtr=True)
serial.timeout = 1
#### 

index = 0
header = True
callsign = "ODZUJF"
date = datetime.now().isoformat()
printer = open(date + "_gps_output_log.txt", 'w') # Creates logfile with current date and time in its name

print("\nSerial port " + sys.argv[1] + " opened. Waiting for GPS-NMEA data...\n") # Prints openning message



try:
    while True: # Infinite loop waiting for data from configured serial port
        try:
            gps_output = ser.readline()

            date = datetime.utcnow().isoformat("T") + "Z"
            print("Received: " + gps_output.rstrip('\n'))
            sentence = make_sentence(gps_output, True)

            if sentence == "wrong_checksum": # Sentence is not uploaded if it didn't pass the checksum, but is still logged
                print "Checksum error - sentence not sent\n"
            elif sentence == "parse_error":
                print "Can't parse data - sentence not sent\n"
            else:
                print("Sending: " + sentence.rstrip('\n'))    # Prints sentence uploading to DB to the terminal              
                
                sentence = b64encode(sentence) # Uploader to DB
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

                response = c.getresponse() # Prints response from DB or checksum error to the terminal
                print "Status:", response.status, response.reason, "\n"  

            if header == True: # Writes HEADER to the logfile
                printer.write("Entry_id,GPS_message_type,Time,Lat,Lat_dir,Lon,Lon_dir,GPS_equal,Num_sats,Horizontal_dil,Altitude,Altitude_units,Geo_sep,Geo_sep_units,Age_gps_data,Ref_station_id,Upload_status\n")
                header = False

            if sentence == "wrong_checksum": # Writes entry to the logfile
                printer.write('{:05}'.format(index) + "," + str(gps_output.rstrip('\n')) + "," + "Wrong_checksum" + "\n")
            elif sentence ==  "parse_error": 
                pass
            else:
                printer.write('{:05}'.format(index) + "," + str(gps_output.rstrip('\n')) + "," + str(response.reason) + "\n")
            
            index += 1

        except serial.SerialException: # Close safely in case of port disconnection
            print "_Error! Closing the port...\n"
            break

except KeyboardInterrupt: # Close safely with "CTRL + C"
    print "_Program closed\n"

printer.close()
