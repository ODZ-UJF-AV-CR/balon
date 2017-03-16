#!/bin/bash
# This expects C920 camera connected on video1
# Switches to use balon first if on odroid, this can't run as root.

DEVICE=0
USER=odroid
OUTF='file/ps:/data/balon/video/'$(date '+%F-%H%M%S.avi')

echo Saving to $OUTF

if [ $( id -u ) == 0 ] 
then
  su -c $0 $USER
else
  v4l2-ctl -d ${DEVICE} --set-fmt-video=width=1920,height=1080,pixelformat=1
  v4l2-ctl -d ${DEVICE} --set-ctrl=focus_auto=0
  v4l2-ctl -d ${DEVICE} --set-ctrl=focus_absolute=0
  time cvlc v4l2:///dev/video${DEVICE}:chroma=h264:width=1920:height=1080:fps=30 --sout $OUTF
fi

