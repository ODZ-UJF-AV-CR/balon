#!/bin/bash

# Acquire images from the webcam in a loop

DELAY=10
RES=1280x720
CAMERA=/dev/video0
DATADIR=/data/balon/img

mkdir -p $DATADIR
# F 5 is better at night
#fswebcam -i 0 -r $RES -D 1 -S 10 -F 1 -l $DELAY --gmt --timestamp "%F %T" --save "img/%F-%T.jpg"
fswebcam -d ${CAMERA} -i 0 -r $RES -D 1 -S 10 -F 1 -l $DELAY --gmt --save "$DATADIR/%F-%H%M%S.jpg"
