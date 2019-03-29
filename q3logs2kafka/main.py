#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import sys

import click

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
def foobar():
    for line in run_command(['docker', 'logs', '-f', 'ioquake3']):
        blob = log_line2blob(line)
        if blob:
            log.info(json.dumps(blob))


if __name__ == '__main__':
    # pylint: disable=E1120
    sys.exit(cli())
