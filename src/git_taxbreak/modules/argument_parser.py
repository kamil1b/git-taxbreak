""" Module provide functionality for args parser
@author Kamil Luczak
"""
import argparse
from os.path import expanduser, expandvars
import sys
from datetime import datetime


def valid_date(s):
    try:
        datetime.strptime(s, "%m/%d/%y")
        return s
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format: {}".format(s))


def valid_output(filename):
    filename = expanduser(expandvars(filename))
    return argparse.FileType("w+")(filename)


class ArgumentParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._configure_parser()
        self._parse_arguments()

    def _configure_parser(self):
        today = datetime.today()
        self._parser.add_argument("-u", "--user", action="store")
        self._parser.add_argument(
            "-U", "--unified", type=int, action="store", default=0
        )
        self._parser.add_argument(
            "-a", "--after", type=valid_date, default=today.strftime("%m/1/%y")
        )
        self._parser.add_argument(
            "-b", "--before", type=valid_date, default=today.strftime("%m/%d/%y")
        )
        self._parser.add_argument(
            "-o", "--output", type=valid_output, default=sys.stdout
        )
        self._parser.add_argument(
            "-t", "--type", type=str, choices=["diff", "file"], default="file"
        )

    def _parse_arguments(self):
        args = self._parser.parse_args()
        self._user = args.user
        self._after = args.after
        self._before = args.before
        self._type = args.type
        self._unified = args.unified
        self._output = args.output

    @property
    def user(self):
        return self._user

    @property
    def after_date(self):
        return self._after

    @property
    def before_date(self):
        return self._before

    @property
    def output(self):
        return self._output

    @property
    def type(self):
        return self._type

    @property
    def unified(self):
        return self._unified
