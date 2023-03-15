#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import sys

import click
from flask import Flask, request, jsonify
from kafka import KafkaProducer
from kafka.errors import KafkaError

log = logging.getLogger(__file__)
app = Flask("event_producer")


def _configure_logging(verbosity):
    loglevel = max(3 - verbosity, 0) * 10
    logging.basicConfig(level=loglevel, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if loglevel >= logging.DEBUG:
        # Disable debugging logging for external libraries
        for loggername in 'urllib3', 'google.auth.transport.requests':
            logging.getLogger(loggername).setLevel(logging.CRITICAL)


@click.command()
@click.option('-v', '--verbosity', help='Verbosity', default=0, count=True)
def cli(verbosity: int):
    _configure_logging(verbosity)

    return app.run()


@app.route("/event/<uuid:match_id>", methods=['PUT'])
def event(match_id):
    response = request.json
    response["match_id"] = match_id
    return jsonify(response)


if __name__ == '__main__':
    # pylint: disable=E1120
    sys.exit(cli())
