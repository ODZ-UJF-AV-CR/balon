#!/bin/bash
# This expects C920 camera connected on video1
# Switches to use balon first if on odroid, this can't run as root.

DEVICE=1
USER=odroid

if [ $( id -u ) == 0 ] 
then
  su -c $0 $USER
else
  v4l2-ctl -d 2 --set-fmt-video=width=1920,height=1080,pixelformat=1
  cvlc v4l2:///dev/video${DEVICE}:chroma=h264:width=1920:height=1080:fps=30 --sout 'file/ps:/data/balon/video/video-test.avi' 
fi
