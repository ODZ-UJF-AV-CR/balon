# habhub telemetry logging and uploading tool 

The python script which receive telemetry packets from radio modem on serial port. The all received data are logged for forensic search. 
Recognised telemetry packets are processed parsed an uploaded to http://habhub.org/ which allows instantaneous tracking of the ballon flight on https://tracker.habhub.org/ tracker map.

The logfile looks like following: 

      Entry_id,Callsign,Time,Lat,Lat_dir,Lon,Lon_dir,GPS_equal,Num_sats,Horizontal_dil,Altitude,Altitude_units,Geo_sep,Geo_sep_units,Age_gps_data,Ref_station_id,Upload_status
    00000,$GPGGA,151225.00,5008.11103,N,01425.81157,E,2,07,1.25,317.1,M,44.3,M,,0000*5E,Forbidden
    00001,$GPGGA,151226.00,5007.11100,N,01425.81136,E,2,07,1.25,317.2,M,44.3,M,,0000*5A,Wrong_checksum
    00002,$GPGGA,151227.00,5008.11098,N,01425.81128,E,2,07,1.25,317.2,M,44.3,M,,0000*54,Forbidden
    00003,$GPGGA,151229.00,5008.11094,N,01425.81092,E,2,08,1.25,317.4,M,44.3,M,,0000*5F,Forbidden
    00004,$GPGGA,151229.00,5008.11094,N,01425.81092,E,2,08,1.25,317.4,M,44.3,M,,0000*5F,Forbidden
    00005,$GPGGA,151230.00,5008.11092,N,01425.81073,E,2,08,1.25,317.5,M,44.3,M,,0000*5F,Forbidden


## The use 

### Prerequisities

The software needs [Pynmea2](https://github.com/Knio/pynmea2) library which could be installed by following command: 

    pip install pymavlnik crc16 serial ttn 

For usage with QGC parallelly, you must install [Mavlink-routered](https://github.com/intel/mavlink-router)
### Program launch

The software needs a hardware radio modem.  The modem is accessed trought an serial port "/dev/ttyUSB0" for example. Then the code could be executed by runnig following command: 

    python habitat_uploader.py /dev/ttyUSB0 rover_calsign

### Program launch with QGC (Mavlink UDP)
    
    mavlink-routered -c mavlink.conf

    pythton python habitat_uploader.py udpin:0.0.0.0:11000 rover_calsign

### Callsign setting

In order to properly display data in HabHub Tracker, the callsign variable in the script must be set to the same value as was earlier configured on Habitat's [Genpayload](http://habitat.habhub.org/genpayload/) webpage. In case the callsign need to be changed, go to Genpayload webpage and under "payload configuration documents" click "start from existing". Then search for the name of your payload (curently set to "LetFik2") and open the latest version of the document (it should be the most bottom one). There under "Parser configuration" choose "edit" and change "Callsign" field to the new value. Don't forget to save this configuration and then also the whole document. Now just simply change the callsign variable in the script to the same value as configured and from now on data should be uploaded and interpreted under new callsign. Note that you don't need to change callsign in order to change the name of the payload.






