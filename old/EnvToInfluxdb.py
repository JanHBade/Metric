#!/usr/bin/python3 -u

from influxdb import InfluxDBClient
from multiprocessing import Process, Queue
import time

import bme280

def f(q):
	while True:
#		try:
			temperature,pressure,humidity = bme280.readBME280All()
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
#		except:
#			print ("Error")
#			time.sleep(10)


