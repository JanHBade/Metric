#!/usr/bin/python3 -u

import json
import os
import socket
import time
import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from multiprocessing import Queue
from influxdb import InfluxDBClient

q = Queue()

def aircraft():
	#print ("air")
	global q	
	
	with open('/var/run/dump1090-fa/aircraft.json') as fd:
		stats = json.load(fd)

	aircraft = len(stats.get('aircraft', []))
	messages = stats.get('messages')
	if messages is None:
		messages = 0
		
	q.put("AdsB,Standort=Dachboden Nachrichten={messages},Flugzeuge={aircraft} {timestamp}".format(messages=messages,
						aircraft=aircraft,
						timestamp=int(time.time())))

def stats():
	#print("stats")
	global q	
	
	with open('/var/run/dump1090-fa/stats.json') as fd:
		stats = json.load(fd)
		
	stats = stats.get('last1min')
	values = stats.get('local')
	signal = values.get('signal')
	if signal is None:
		signal = 0
	noise = values.get('noise')
	if noise is None:
		noise = 0
	
	q.put("AdsB,Standort=Dachboden Signal={signal},Rauschen={noise} {timestamp}".format(signal=signal,
						noise=noise,
						timestamp=int(time.time())))

def on_modified(event):
	#print(f"hey buddy, {event.src_path} has been modified")
	if "aircraft" in event.src_path:
		aircraft()
		
	if "stats" in event.src_path:
		stats()

if __name__ == '__main__':	  
	

	my_event_handler = PatternMatchingEventHandler("*.json", "", True, False)
	my_event_handler.on_modified = on_modified
	
	observer = Observer()
	observer.schedule(my_event_handler, '/var/run/dump1090-fa/')
	observer.start()

	while True:
		#try:
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
		#except:
		#	print ("Error")
		#	time.sleep(10)

