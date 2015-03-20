#!/usr/bin/env python

import serial
import sys

ser=serial.Serial('/dev/ttyUSB0',115200)

print("Connecting to USB ??")
print "Input(Y or N) : ",sys.argv[1]
ser.write(sys.argv[1])


