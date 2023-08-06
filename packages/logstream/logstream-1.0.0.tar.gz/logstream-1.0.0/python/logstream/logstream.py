#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""logstream: command."""

from __future__ import absolute_import

__version__ = '1.0.0'

import sys
from subprocess import Popen, PIPE, STDOUT
import time

if sys.version_info[0] < 3:
    raise Exception("Python 3 Please")

usage = "Usage: " + sys.argv[0] + """

    --help
    --version
    --format [type]

    os darwin:
        [default|compact|json|ndjson|syslog]

    os linux:
        [short|short-full|short-unix|verbose|export]
        [json|json-pretty|json-sse|json-seq]

    os windows:
        TODO

    --tail file

"""


def stream(formatting=None):
    """stream: operating systems syslog data stream."""
    if sys.platform == 'darwin':
        if formatting is None:
            formatting = 'ndjson'
        cmd = ['log', 'stream', '--style', formatting]
    elif sys.platform in ('linux', 'linux2'):
        if formatting is None:
            formatting = 'json'
        cmd = ['journalctl', '-f', '-o', formatting]
    else:
        print('No log stream.  No such platform ' + str(sys.platform))
        return False

    with Popen(cmd, shell=False, stdout=PIPE, stderr=PIPE) as _f:
        while True:
            line = _f.stdout.readline()
            if not line:
                time.sleep(1)
            else:
                yield line
            sys.stdout.flush()

    return True


def tail(file):
    """tail: operating systems tail follow file command."""
    if sys.platform == 'darwin':
        cmd = ['tail', '-0', '-F', file]
    elif sys.platform in ('linux', 'linux2'):
        cmd = ['tail', '-n', '0', '-F', file]
    else:
        cmd = ['tail', '-F', file]

    try:
        with Popen(cmd, shell=False, stdout=PIPE, stderr=STDOUT) as _f:
            while (_f.returncode is None):
                line = _f.stdout.readline()
                if not line:
                    time.sleep(1)
                else:
                    yield line
                sys.stdout.flush()

    except Exception as _e:
        print('Exception ' + str(_e))
        return False

    return True


def main():
    """main: app."""
    try:
        if sys.argv[1:]:
            if sys.argv[1] == "--help":
                print(usage)
            elif sys.argv[1] == "--version":
                print(__version__)
            elif sys.argv[1] == "--format":
                try:
                    formatting = sys.argv[2]
                except IndexError:
                    formatting = None
                for line in stream(formatting):
                    print(line)
            elif sys.argv[1] == "--tail":
                try:
                    file = sys.argv[2]
                except IndexError:
                    file = None
                for line in tail(file):
                    print(line)
            else:
                print(usage)
        else:
            for line in stream():
                print(line)
    except KeyError as _e:
        print("KeyError: " + str(_e))
        sys.exit(1)


if __name__ == '__main__':
    main()
