#!/usr/bin/python3 -u

import time
import json

import board
import busio
import adafruit_bme280

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

from paho.mqtt import client as mqtt_client
client = mqtt_client.Client()

if __name__ == '__main__':	
	client.connect("Isis")

	while True:
		data = {}
		data["Temperatur"]=bme280.temperature
		data["Druck"]=bme280.pressure
		data["Feuchte"]=bme280.humidity

		client.publish("SPS/Dachboden",json.dumps(data))

		time.sleep(59)
