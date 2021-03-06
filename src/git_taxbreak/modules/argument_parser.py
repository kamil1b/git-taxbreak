""" Module provide functionality for args parser
@author Kamil Luczak
"""
import argparse
import datetime
from os.path import expanduser, expandvars

DEFAULT_OUTPUT = "artifacts.zip"


def valid_date(s):
    try:
        datetime.datetime.strptime(s, "%m/%d/%y")
        return s
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format: {}".format(s))


def valid_output(filename):
    filename = expanduser(expandvars(filename))
    argparse.FileType("w+")(filename)
    return filename


class ArgumentParser:
    """Class response for parse arguments provide to aplication
    """

    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._configure_parser()
        self._parse_arguments()

    def _configure_parser(self):
        today = datetime.datetime.today()
        self._parser.add_argument("-u", "--user", action="store")

        self._parser.add_argument(
            "-a", "--after", type=valid_date, default=today.strftime("%m/1/%y")
        )
        self._parser.add_argument(
            "-b", "--before", type=valid_date, default=today.strftime("%m/%d/%y")
        )
        self._parser.add_argument(
            "-o", "--output", type=valid_output, default=DEFAULT_OUTPUT
        )

    def _parse_arguments(self):
        args = self._parser.parse_args()
        self._user = args.user
        self._after = args.after
        self._before = args.before
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
