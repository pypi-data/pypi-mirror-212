
# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

from setuptools import setup

setup(
    name = "logstream",
    packages = ["logstream"],
    entry_points = {
        "console_scripts": ['logstream = logstream.logstream:main']
        },
    version = '1.0.0',
    description = "operating system syslog data and/or tail log files.",
    long_description = "Python command line tool to logstream operating syslog data and/or log files.",
    author = "Karl Rink",
    author_email = "karl@rink.us",
    url = "https://gitlab.com/krink/logstream",
    install_requires = []
    )
