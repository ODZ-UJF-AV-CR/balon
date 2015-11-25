#!/bin/bash

#SYSRTC=$( date "+%Y-%m-%d %H:%M:%S" )
GPSDATA=$(./gpsline.py)

echo Got GPSdata

echo "$GPSDATA" | gammu sendsms TEXT +420777642401
