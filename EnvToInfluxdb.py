#!/usr/bin/python3 -u

import time
from influxdb import InfluxDBClient
from multiprocessing import Process, Queue

import board
import busio
import adafruit_bme280

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

def f(q):
	while True:
#		try:
			temperature = bme280.temperature
			pressure = bme280.pressure
			humidity = bme280.humidity
			q.put("Umgebung,Standort=Dachboden,Sensor=BME280 Temperatur={temperature},Feuchte={humidity},Luftdruck={pressure} {timestamp}"
					.format(temperature=temperature,
							humidity=humidity,
							pressure=pressure,
							timestamp=int(time.time())))
#		except:
#			print ("Error")
#			time.sleep(4)

			time.sleep(10)

if __name__ == '__main__':
	
	q = Queue()
	p = Process(target=f, args=(q,))
	p.start()

	while True:
#		try:
			client = InfluxDBClient(host='Nehebkau', port=8086)
			client.create_database('Metric')
			while True:
				if q.qsize() > 20:
					data = []
					for x in range(20):
						data.append(q.get())
					client.write_points(data, database='Metric', time_precision='s', batch_size=100, protocol='line')
				else:
					time.sleep(5)

#while True:
#	print("\nTemperature: %0.1f C" % bme280.temperature)
#	print("Humidity: %0.1f %%" % bme280.humidity)
#	print("Pressure: %0.1f hPa" % bme280.pressure)
#	print("Altitude = %0.2f meters" % bme280.altitude)
#	time.sleep(2)