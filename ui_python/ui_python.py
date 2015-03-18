#!/usr/bin/env python

import serial

ser=serial.Serial('/dev/ttyUSB0',115200)
#print ser.read()
while 1:
  print("Connecting to USB ??")
  try:
    x=raw_input("Input(Y or N) : ")
    ser.write(x)
  except KeyboardInterrupt:
    print("")
    break

