#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import sys

import click
from kafka import KafkaProducer
from kafka.errors import KafkaError

from core import log_line2blob, run_command

log = logging.getLogger(__file__)


def _configure_logging(verbosity):
    loglevel = max(3 - verbosity, 0) * 10
    logging.basicConfig(level=loglevel, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if loglevel >= logging.DEBUG:
        # Disable debugging logging for external libraries
        for loggername in 'urllib3', 'google.auth.transport.requests':
            logging.getLogger(loggername).setLevel(logging.CRITICAL)


@click.group()
@click.option('-v', '--verbosity', help='Verbosity', default=0, count=True)
def cli(verbosity: int):
    _configure_logging(verbosity)

    log.info('I am an informational log entry in the sample script.')
    return 0


@cli.command(name='tail')
@click.option('-c', '--command', help='command to gather logs', type=str, required=True)
@click.option('-b', '--bootstrap-server', help='kafka bootstrap server:port', type=str, required=True, multiple=True)
@click.option('-t', '--topic', help='kafka topic', type=str, required=True)
def foobar(command: str, bootstrap_server: list, topic: str):
    producer = KafkaProducer(
        value_serializer=lambda m: json.dumps(m).encode('ascii'), bootstrap_servers=bootstrap_server)

    for line in run_command(command.split()):
        blob = log_line2blob(line)
        if blob:
            log.info(json.dumps(blob))
            future = producer.send(topic, blob)
            # Block for 'synchronous' sends
            try:
                record_metadata = future.get(timeout=10)
            except KafkaError:
                log.exception()
            pass


if __name__ == '__main__':
    # pylint: disable=E1120
    sys.exit(cli())
