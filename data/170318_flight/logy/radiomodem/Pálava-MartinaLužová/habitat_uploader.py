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


######################## CALLSIGN SETTINGS ########################

callsign = "LetFik2"

###################################################################


def make_sentence(sentence, checksum_bool): # Function which takes NMEA sentence as an argument
                                            # and returns sentence suitable for uploading to DB
    if sentence[:6] != "$GPGGA":
        return "parse_error"
    try:
        try: 
            if checksum_bool == False:
                parsed = pynmea2.parse(sentence[:-4], checksum_bool)
            else:
                parsed = pynmea2.parse(sentence)
        except pynmea2.ChecksumError:
            return "checksum_error"
    except pynmea2.nmea.ParseError:
        return "parse_error"
    
    if None in (parsed.timestamp, parsed.lat, parsed.lat_dir, parsed.lon, parsed.lon_dir, parsed.altitude, parsed.num_sats):
        return "gps_no_fix" 

    if parsed.lat_dir == 'S':
        parsed.lat = str(float(parsed.lat) * (-1))
    if parsed.lon_dir == 'W':
        parsed.lon = str(float(parsed.lon) * (-1))

    # Creates new sentence in format configured on Habitat's webpage
    new_sentence = callsign + ",%s,%s,%s,%s,%s,%s,%s" % (parsed.timestamp, parsed.lat, parsed.lon, parsed.altitude, parsed.num_sats, noise, flux)
    new_sentence = "$$" + new_sentence + "*" + str(checksum(new_sentence)) + '\n'
    return(new_sentence)


def make_data(sentence, callsign): # Creates data in format suitable for upload to DB
    sentence = b64encode(sentence) 
    data = {
        "type": "payload_telemetry",
        "data": {
            "_raw": sentence
            },
        "receivers": {
            callsign: {
                "time_created": get_date(True),
                "time_uploaded": get_date(True),
                },
            },
    }
    return data


def checksum(sentence): # Returns crc16-citt checksum of ASCII string
    crc = crc16.crc16xmodem(sentence, 0xffff)
    return ('{:04X}'.format(crc))


def get_date(format_bool):
    if format_bool == True:
        return (datetime.utcnow().isoformat("T") + "Z")
    else:
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")



if len(sys.argv) < 2: # Terminate program, if run without defining port as an argument
    print "Usage: python %s [recv port]" % sys.argv[0]
    sys.exit()


ser = serial.Serial(sys.argv[1], rtscts=True, dsrdtr=True)
serial.timeout = 1

index, index_raw, index_candy, noise, flux = (0, 0, 0, 0, 0)
time, latitude, longtitude, altitude = (0, 0, 0, 0)
date = get_date(False)

printer = open(date + "_parsed_balloon_output_log", 'w') # Creates logfile of sucesfully parsed sentences with current date and time in its name
printer_raw = open(date + "_raw_balloon_output_log.txt", 'w') # Creates logfile of all received data
printer_candy = open(date + "_candy_detector_log", 'w')
 # Writes HEADER to the logffile
printer.write("Entry_id,GPS_message_type,Time,Lat,Lat_dir,Lon,Lon_dir,GPS_equal,Num_sats,Horizontal_dil,Altitude,Altitude_units,Geo_sep,Geo_sep_units,Age_gps_data,Ref_station_id,Upload_status\n")
printer_raw.write("Entry_id,GPS_message_type,Time,Lat,Lat_dir,Lon,Lon_dir,GPS_equal,Num_sats,Horizontal_dil,Altitude,Altitude_units,Geo_sep,Geo_sep_units,Age_gps_data,Ref_station_id,Upload_status\n")
printer_candy.write("Entry_id,Time,Latitude,Longtitude,Altitude,Candy__detector_data,,,,,\n")

print("\nSerial port " + sys.argv[1] + " opened. Waiting for GPS-NMEA data...\n") # Prints openning message

try:
    while True: # Infinite loop waiting for data from configured serial port
        try:
            gps_output = ser.readline().rstrip('\n\r')
            
            if gps_output[0] == "\r":
                gps_output = gps_output[1:]

            print("Received: " + gps_output)

            if gps_output[:6] == "$CANDY":
                candy_data = gps_output.split(",")
                noise = candy_data[2]
                flux = candy_data[3]
                printer_raw.write(('{:05}'.format(index_raw) + "," + gps_output + "," + "Candy_detector_data" + "\n"))
                printer_candy.write('{:05}'.format(index_candy) + "," + time + "," + latitude + "," + longtitude + "," + altitude + "," + gps_output + "\n")
                print "Candy detector data logged\n"
                index_candy += 1
                index_raw += 1
           
            else:
                sentence = make_sentence(gps_output, True)
                
                if sentence == "parse_error": # If sentence couldn't be parsed, it is not uploaded and is logged only to raw logfile
                    print "Can't parse data - sentence not sent\n"
                    printer_raw.write('{:05}'.format(index_raw) + "," + gps_output + "," + "Parse_error" + "\n")
                    index_raw += 1
                elif sentence == "checksum_error": # Sentence is not uploaded, if it didn't pass the checksum, but is still logged
                    print "Checksum error - sentence not sent\n"
                    printer_raw.write('{:05}'.format(index_raw) + "," + gps_output + "," + "Checksum_error" + "\n")
                    index_raw += 1
                elif sentence == "gps_no_fix": # If NMEA data was uncomplete (without GPS fix), sentence it is not uploaded and is logged only to raw logfile
                    print "Uncomplete NMEA data (no GPS fix) - sentence not sent\n"
                    printer_raw.write('{:05}'.format(index_raw) + "," + gps_output + "," + "No_GPS_fix" + "\n")
                    index_raw += 1
                else:
                    split_sentence = sentence.split(",")
                    time = split_sentence[1]
                    latitude = split_sentence[2]
                    longtitude = split_sentence[3]
                    altitude = split_sentence[4] 

                    print("Sending: " + sentence.rstrip('\n'))    # Prints sentence uploading to DB to the terminal              
                    
                    for x in range(0,4):
                        try:
                            c = httplib.HTTPConnection("habitat.habhub.org") # DB uploader
                            c.request(
                                "PUT",
                                "/habitat/_design/payload_telemetry/_update/add_listener/%s" % sha256(b64encode(sentence)).hexdigest(),
                                json.dumps(make_data(sentence, callsign)),  # BODY
                                {"Content-Type": "application/json"}  # HEADERS
                                )

                            response = c.getresponse() # Prints response from DB

                            print "Status:", response.status, response.reason, "\n" # Prints response from DB and creates log entry
                            printer.write('{:05}'.format(index) + "," + gps_output + "," + str(response.reason) + "\n")
                            printer_raw.write('{:05}'.format(index_raw) + "," + gps_output + "," + str(response.reason) + "\n")
                            index_raw += 1
                            index += 1
                            break

                        except Exception:
                            if x < 3:
                                print "No internet connection. Repeating upload... [" + str(x + 1) +"/3]" # In case of no internet connection repeats upload three times
                            else:
                                print "Error! No internet connection - sentence not sent\n" # If after three tries is sentence not uploaded, create log entry and continue
                                printer.write('{:05}'.format(index) + "," + gps_output + "," + "Upload_error" + "\n")
                                printer_raw.write('{:05}'.format(index_raw) + "," + gps_output + "," + "Upload_error" + "\n")
                                index_raw += 1
                                index += 1
                
        except serial.SerialException: # Close safely in case of port disconnection
            print "Error! Device disconnected. Reconnect device and restart program.\n"
            break

except KeyboardInterrupt: # Close safely with "CTRL + C"
    print "_Program closed\n"

printer.close()
printer_raw.close()
printer_candy.close()
