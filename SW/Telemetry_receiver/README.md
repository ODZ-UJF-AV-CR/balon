# habhub telemetry logging and uploading tool 

The python script which receive telemetry packets from radio modem on serial port. The all received data are logged for forensic search. 
Recognised telemetry packets are processed parsed an uploaded to http://habhub.org/ which allows instantaneous tracking of the ballon flight on https://tracker.habhub.org/ tracker map.


## The use 

### Prerequisities

The software needs [Pynmea2](https://github.com/Knio/pynmea2) library which could be installed by following command: 

    pip install pynmea2 crc16

### Program launch

The software needs a hardware radio modem.  The modem is accessed trought an serial port "/dev/ttyUSB0" for example. Then the code could be executed by runnig following command: 

    python habitat_uploader.py /dev/ttyUSB0






