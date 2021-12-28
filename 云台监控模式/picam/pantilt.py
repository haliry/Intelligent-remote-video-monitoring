#!/usr/bin/env python

import smbus
import time

bus = smbus.SMBus(1)
addr = 0x40

def scale(x, in_min, in_max, out_min, out_max):
	return (x - in_min)*(out_max - out_min)/(in_max - in_min) + out_min

## enable the PC9685 and enable autoincrement
bus.write_byte_data(addr, 0, 0x20)
bus.write_byte_data(addr, 0xfe, 0x1e)

bus.write_word_data(addr, 0x06, 0)
bus.write_word_data(addr, 0x08, 1250)

bus.write_word_data(addr, 0x0a, 0)
bus.write_word_data(addr, 0x0c, 1250)

while True:
	pipein = open("/var/www/picam/FIFO_pipan", 'r')
	line = pipein.readline()
	line_array = line.split(' ')
	if line_array[0] == "servo":
		pan_setting = scale(int(line_array[1]),110, 260, 833, 1667)
		tilt_setting = scale(int(line_array[2]), 130, 270, 833, 1667)
		#bus.write_word_data(addr, 0x08, pan_setting)
		#bus.write_word_data(addr, 0x0c, tilt_setting)
		bus.write_word_data(addr, 0x0c, pan_setting)
		bus.write_word_data(addr, 0x08, tilt_setting)
	pipein.close()
