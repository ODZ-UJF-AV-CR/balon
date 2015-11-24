#!/bin/bash

fswebcam -r 1600x1200 -D 1 -S 10 -F 5 --save shot.jpg && qiv shot.jpg
