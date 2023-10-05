#!/usr/bin/python3 -u

import json
import os
import socket
import time
import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from paho.mqtt import client as mqtt_client

client = mqtt_client.Client()

def aircraft():
    #print ("air")

    with open('/var/run/dump1090-fa/aircraft.json') as fd:
        stats = json.load(fd)

        try:
            client.publish("adsb/Wosret/aircraft/raw",json.dumps(stats))
        except:
            print("Error: air raw")

        aircraft = len(stats.get('aircraft', []))
        messages = stats.get('messages')
        if messages is None:
            messages = 0

        newjson = {}
        newjson["aircraft"] = aircraft
        newjson["messages"] = messages
        try:
            client.publish("adsb/Wosret/aircraft",json.dumps(newjson))
        except:
            print("Error: pub air")

def stats():
    #print("stats")

    with open('/var/run/dump1090-fa/stats.json') as fd:
        stats = json.load(fd)

        try:
            client.publish("adsb/Wosret/stats/raw",json.dumps(stats))
        except:
            print("Error stat raw")

        stats1min = stats.get('last1min')
        values = stats1min.get('local')
        signal = values.get('signal')
        if signal is None:
            signal = 0
        noise = values.get('noise')
        if noise is None:
            noise = 0

        newjson = {}
        newjson["signal"] = signal
        newjson["noise"] = noise
        try:
            client.publish("adsb/Wosret/stats",json.dumps(newjson))
        except:
            print("Error: pub Stats")

def on_modified(event):
    #print(f"hey buddy, {event.src_path} has been modified")
    if "aircraft" in event.src_path:
        aircraft()

    if "stats" in event.src_path:
        stats()

if __name__ == '__main__':
    client.connect("Isis")

    my_event_handler = PatternMatchingEventHandler("*.json", "", True, False)
    my_event_handler.on_modified = on_modified

    observer = Observer()
    observer.schedule(my_event_handler, '/var/run/dump1090-fa/')
    observer.start()

    while True:
        client.reconnect()
        client.loop()

        time.sleep(1)
