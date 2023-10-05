#!/usr/bin/env python3

from influxdb import InfluxDBClient
import random
import time

import bme280

print(time.time())

client = InfluxDBClient(host='Nehebkau', port=8086)

#(chip_id, chip_version) = bme280.readBME280ID() 

print(time.time())

data = []
for x in range(50):
	temperature,pressure,humidity = bme280.readBME280All()
	data.append("Environment,sensor=BME280,chip_id=96,chip_version=0 Temperature={temperature},Humidity={humidity},Pressure={pressure} {timestamp}"
			.format(temperature=temperature,
					humidity=humidity,
					pressure=pressure,
					timestamp=int(time.time())))
	time.sleep(1)

print(time.time())

client.write_points(data, database='Metric', time_precision='s', batch_size=100, protocol='line')

print(time.time())
