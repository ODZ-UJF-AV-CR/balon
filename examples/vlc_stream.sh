#!/bin/bash
# This expects C920 camera connected on video0 and assumes local IP is 10.1.1.127
# Run vlc http://<ip-of-odroid>:8100 to see camera stream from remote host
# Switches to use balon first if on odroid, this can't run as root.
if [ $( id -u ) == 0 ] 
then
  su -c $0 balon
fi

cvlc v4l2:///dev/video0:chroma=h264:width=1920:height=1080 --sout '#standard{access=http,mux=ts,dst=10.1.1.127:8100,name=stream,mime=video/ts}' -vvv
