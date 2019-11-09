""" Tool for collect artifacts for taxbreak program
@author Kamil Luczak
"""
from os import getcwd

from git import Repo

from .modules.argument_parser import ArgumentParser
from .modules.artifacts_collector import Collector
from .modules.writter import Writter


def read_user(repo):
    with repo.config_reader() as reader:
        if "user" in reader.sections():
            return next((v for k, v in reader.items("user") if k == "name"), None)
    return None


def main():
    try:
        parser = ArgumentParser()
    except TypeError as error:
        print(error)
        exit(1)
    repo = Repo(getcwd(), search_parent_directories=True)
    user = parser.user or read_user(repo)
    artifacts = Collector(
        repo, user, parser.after_date, parser.before_date, parser.unified
    ).Artifacts
    Writter.archive(parser.output, artifacts)
