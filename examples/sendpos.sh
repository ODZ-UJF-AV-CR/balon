#!/bin/bash

#SYSRTC=$( date "+%Y-%m-%d %H:%M:%S" )

# Get line with GPS coordinates
GPSDATA=$(timeout -k 10s 30s ./gpsline.py)
SENDTIMEOUT="60s"
DEST=+420777642401

if [ "x$GPSDATA" == "x" ]; then
   echo No fix, no fun.
else 
   echo Got GPSdata: $GPSDATA
   echo Trying to send for $SENDTIMEOUT
   echo $GPSDATA | timeout -k 5s $SENDTIMEOUT gammu sendsms TEXT $DEST 
fi
