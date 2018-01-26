#!/usr/bin/env python
import sys
import httplib
import json
import crc16
from base64 import b64encode
from hashlib import sha256
from datetime import datetime
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse



######################## CALLSIGN SETTINGS ########################

callsign = "LetFik3"

###################################################################



def get_query_field(url, field):
    """
    Given a URL, return a list of values for the given ``field`` in the
    URL's query string.
    
    >>> get_query_field('http://example.net', field='foo')
    []
    
    >>> get_query_field('http://example.net?foo=bar', field='foo')
    ['bar']
    
    >>> get_query_field('http://example.net?foo=bar&foo=baz', field='foo')
    ['bar', 'baz']
    """
    try:
        return urlparse.parse_qs(urlparse.urlparse(url).query)[field]
    except KeyError:
        return []

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


def sigfox_decode(sigfoxmsg):

    lat = int(sigfoxmsg[0:6], 16) 
    lon = int(sigfoxmsg[6:12], 16)
    h = int(sigfoxmsg[12:16], 16)
    tmcu = int(sigfoxmsg[16:20], 16)
    vaccu = int(sigfoxmsg[20:24], 16)
    
    tmcu =  0.171417*tmcu - 279.38
    vaccu = (5.681*3.3 / 4096.0) * vaccu
    lat = lat * 360.0 / 16777216.0
    lon = lon * 360.0 / 16777216.0
    
    return({"latitude":lat,"longitude":lon, "elevation":h, "MCU_temp":tmcu, "bat_voltage":vaccu})


class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        data = get_query_field(self.path,field='data')

        if data != []:
            telemetry_data = sigfox_decode(data[0])

            time = datetime.utcnow().strftime("%H:%M:%S")
            latitude = telemetry_data["latitude"]
            longitude = telemetry_data["longitude"]
            altitude = telemetry_data["elevation"] 

            temperature = telemetry_data["MCU_temp"] 
            voltage = telemetry_data["bat_voltage"] 


            web_message = '\n'.join([
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                    self.address_string()),
                'command=%s' % self.command,
                'query_value=%s' % get_query_field(self.path,field='data'),
                'request_version=%s' % self.request_version,
                'time=%s' % time,
                'latitude=%s' % latitude,
                'longitude=%s' % longitude,
                'altitude=%s' % altitude,
                'MCU_temp=%s' % temperature,
                'battery_voltage=%s' % voltage,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                ])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(web_message)

            # Creates new sentence in format configured on Habitat's webpage
            sentence = callsign + ",%s,%s,%s,%s,%s,%s" % (time, latitude, longitude, altitude, temperature, voltage)
            sentence = "$$" + sentence + "*" + str(checksum(sentence)) + '\n'


            print("Sending: " + sentence.rstrip('\n'))    # Prints sentence uploading to DB to the terminal              
            
            c = httplib.HTTPConnection("habitat.habhub.org") # DB uploader
            c.request(
                "PUT",
                "/habitat/_design/payload_telemetry/_update/add_listener/%s" % sha256(b64encode(sentence)).hexdigest(),
                json.dumps(make_data(sentence, callsign)),  # BODY
                {"Content-Type": "application/json"}  # HEADERS
                )

            response = c.getresponse() # Prints response from DB
            printer.write(str(datetime.utcnow()) + "," + str(latitude) + "," + str(longitude)+ "," + str(altitude)+ "," + str(temperature)+ "," + str(voltage) + "," + str(response.reason) + "\n")
            printer_raw.write(str(datetime.utcnow()) + "," + str(data[0]) + "," + str(response.reason) + "\n")

            print "Status:", response.status, response.reason, "\n" # Prints response from DB and creates log entry


        else:

            web_message = '\n'.join([
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                    self.address_string()),
                'command=%s' % self.command,
                'query_value=%s' % get_query_field(self.path,field='data'),
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                ])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(web_message)

        return

if len(sys.argv) < 2: # Terminate program, if run without defining port as an argument
    print "Usage: python %s [callsign]" % sys.argv[0]
    sys.exit()

callsign = sys.argv[1]
date = get_date(False)


printer = open(date + "_parsed_balloon_output_log", 'w') # Creates logfile of sucesfully parsed sentences with current date and time in its name
printer_raw = open(date + "_raw_balloon_output_log.txt", 'w') # Creates logfile of all received data

 # Writes HEADER to the logffile
printer.write("Time, Lat, Lon, Altitude, MCU_temp, Battery, Upload_status\n")
printer_raw.write("Time, Sigfox_message, Upload_status\n")

server = HTTPServer(('', 8080), GetHandler)
print 'Starting server at http://localhost:8080'
server.serve_forever()

printer.close()
printer_raw.close()