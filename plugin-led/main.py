import time
import json
import urllib2
import serial
import struct
URL = "http://127.0.0.1:8080/"
ser = serial.Serial('/dev/tty.wchusbserial1420', 9600)

while True:
    data = json.load(urllib2.urlopen(URL))
    det_mood = data['data']['main_mood']
    byte_mood = struct.pack("B", int(det_mood*255))
    ser.write(byte_mood)
    time.sleep(1/20.0)

ser.close()