#!/bin/bash
# Reset the modem using GPIO pins

GPIO_MODE_PATH="/sys/class/gpio/gpio204/direction"
GPIO_EXPORT_PATH='/sys/class/gpio/export'
GPIO_PIN_PATH='/sys/class/gpio/gpio204/value'

if [ ! -d /sys/class/gpio/gpio204 ] ; then
   echo Exporting the GPIO pin
   echo "204" >$GPIO_EXPORT_PATH
fi

if [ ! -d /sys/class/gpio/gpio204 ] ; then
   echo "GPIO pin export did not work"
   exit 1
else
   echo GPIO pin is reachable via the file system
fi

echo "out" >$GPIO_MODE_PATH

# Comment this out to just assure modem is on
echo Resetting modem
echo 0 >$GPIO_PIN_PATH
sleep 2 

# Let the modem run
echo 1 >$GPIO_PIN_PATH
