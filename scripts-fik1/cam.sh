#!/bin/bash

# Acquire images from the webcam in a loop

DELAY=10
RES=1600x1200
RES=1280x960
RES=1280x720

# F 5 is better at night
mkdir -p img
fswebcam -r $RES -D 1 -S 10 -F 1 -l $DELAY --gmt --timestamp "%F %T" --save "img/%F-%T.jpg"
