
import serial

ser=serial.Serial('/dev/ttyUSB0',115200)
while 1:
 string=ser.readline()
 print(string)
 x=raw_input("Input: ")
 print(x)
 ser.write(x)

