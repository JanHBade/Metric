#!/usr/bin/env python3

import json
import os
import socket
import time

def print_aircraft(stats):
    ''' Parse and emit information from the aircraft.json file. '''
    aircraft = len(stats.get('aircraft', []))
    messages = stats.get('messages')
    if not messages:
        raise ValueError('JSON stats undefined')

    m = "PUTVAL \"{}/dump1090/counter-messages\" interval={} N:{}".format(
        hostname,
        interval,
        messages
    )
    print(m)

    m = "PUTVAL \"{}/dump1090/gauge-aircraft\" interval={} N:{}".format(
        hostname,
        interval,
        aircraft
    )
    print(m)


def print_stats(stats):
    ''' Parse and emit information from the stats.json file. '''
    counters = [
        'samples_processed',
        'samples_dropped',
    ]

    gauges = [
        'signal',
        'noise'
    ]

    values = stats.get('local')
    if not values or not type(values) == dict:
        raise ValueError('JSON stats undefined')

    for k in counters:
        value = values.get(k)
        if not value:
            value = 'U'

        m = "PUTVAL \"{}/dump1090/counter-{}\" interval={} N:{}".format(
            hostname,
            k,
            interval,
            value
        )
        print(m)

    for k in gauges:
        value = values.get(k)
        if not value:
            value = 'U'

        m = "PUTVAL \"{}/dump1090/gauge-{}\" interval={} N:{}".format(
            hostname,
            k,
            interval,
            value
        )
        print(m)


if __name__ == '__main__':
    interval = 1
    hostname = 'Test'

    while True:
        with open('/var/run/dump1090-fa/stats.json') as fd:
            stats = json.load(fd)

        stats = stats.get('total')
        print_stats(stats)

        with open('/var/run/dump1090-fa/aircraft.json') as fd:
            stats = json.load(fd)

        print_aircraft(stats)
        time.sleep(interval)