#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import queue
import signal
import sys
import time
from threading import Thread

import click
from flask import Flask, request, Response
# from kafka import KafkaProducer
# from kafka.errors import KafkaError

log = logging.getLogger(__file__)
app = Flask("event_producer")
event_queue = queue.Queue()


def _configure_logging(verbosity):
    loglevel = max(3 - verbosity, 0) * 10
    logging.basicConfig(level=loglevel, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if loglevel >= logging.DEBUG:
        # Disable debugging logging for external libraries
        for loggername in 'urllib3', 'google.auth.transport.requests':
            logging.getLogger(loggername).setLevel(logging.CRITICAL)


class QueueHandler:
    RUN = True

    def shutdown(self, *args):
        log.debug("received signal")
        self.RUN = False

        #ToDo: this needs to get fixed to handle shutdown events and flush the queue befor shutting down

    def write_events_to_kafka(self):
        while True:
            item = None
            try:
                item = event_queue.get(timeout=1)
            except queue.Empty:
                if not self.RUN:
                    break
                time.sleep(0.01)
            if item:
                print(json.dumps(item))


@click.command()
@click.option('-v', '--verbosity', help='Verbosity', default=0, count=True)
def cli(verbosity: int):
    _configure_logging(verbosity)

    q_handler = QueueHandler()
    thread = Thread(target=q_handler.write_events_to_kafka, daemon=True)
    thread.start()
    app.run()


@app.route("/event/<uuid:match_id>", methods=['PUT'])
def handle_event(match_id):
    event = request.json
    event['match_id'] = str(match_id)
    try:
        event_queue.put(request.json)
    except queue.Full:
        log.error("Event queue is full, dropping event.")
        return Response("{}", status=503, mimetype='application/json')

    return Response("{}", status=201, mimetype='application/json')


if __name__ == '__main__':
    # pylint: disable=E1120
    sys.exit(cli())
