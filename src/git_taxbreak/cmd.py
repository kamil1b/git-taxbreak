""" Tool for collect artifacts for taxbreak program
@author Kamil Luczak
"""
import sys
from os import getcwd

from git import Repo

from .modules.argument_parser import ArgumentParser
from .modules.artifacts_collector import Collector
from .modules.writter import Writter


def read_user(repo):
    """ Returns  user name read from repository config

    :param repo: repository
    :type repo: git.Repo, mandatory
    :return:
    :rtype: str, None if user name not found
    """
    with repo.config_reader() as reader:
        if "user" in reader.sections():
            return next((v for k, v in reader.items("user") if k == "name"), None)
    return None


def main():
    """ Program main loop """
    try:
        parser = ArgumentParser()
    except TypeError as error:
        print(error)
        sys.exit(1)
    repo = Repo(getcwd(), search_parent_directories=True)
    user = parser.user or read_user(repo)
    artifacts = Collector(
        repo, user, parser.after_date, parser.before_date, parser.unified
    ).artifacts
    with Writter(parser.output) as writter:
        writter.archive(artifacts)
