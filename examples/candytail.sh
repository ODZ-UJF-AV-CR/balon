#!/bin/bash
# Show two last (hopefully) records from Candy on COM4
cat </dev/ttyUSB3 | cut -f 544- -d ,
