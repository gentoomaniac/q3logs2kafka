#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import uuid
import sys
import urllib.parse

import click
import requests

from q3logs_reader.core import log_line2blob, run_command

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

    return 0


@cli.command(name='tail')
@click.option('-c', '--command', help='command to gather logs', type=str, required=True)
@click.option('-u', '--url', help="URL that events will be sent to", type=str, required=True)
def tail(command: str, url: str):
    headers = {'content-type': 'application/json'}
    timeout = 10

    match_id = str(uuid.uuid4())
    for line in run_command(command.split()):
        blob = log_line2blob(line)
        if blob:
            if blob['event'] == "loaded map":
                response = requests.put(urllib.parse.urljoin(url, match_id),
                                        data=json.dumps({'event': 'GameEnded'}),
                                        timeout=timeout,
                                        headers=headers)
                if response.status_code != 201:
                    log.error("failed sending GameEnded: %s", response.text)
                match_id = str(uuid.uuid4())

            response = requests.put(urllib.parse.urljoin(url, match_id),
                                    data=json.dumps(blob),
                                    timeout=timeout,
                                    headers=headers)
            #ToDo: check status code
            if response.status_code != 201:
                log.error("failed sending event: %s", response.text)


if __name__ == '__main__':
    # pylint: disable=E1120
    sys.exit(cli())
