""" Tool for collect artifacts for taxbreak program
@author Kamil Luczak
"""
import os
from unicodedata import normalize
from zipfile import ZipFile
from git import Repo
from .modules.argument_parser import ArgumentParser


def read_user(repo):
    with repo.config_reader() as reader:
        if "user" in reader.sections():
            return next((v for k, v in reader.items("user") if k == "name"), None)
    return None


def get_commits(repo, user, after, before):
    commits = repo.git.log(
        "--all", "--reverse", format="%H", author=user, after=after, before=before
    ).split("\n")
    if "" in commits:
        commits.remove("")
    return commits


def get_diffs(repo, commits, unified):
    return "\n\n".join(
        normalize("NFKD", repo.git.show("-w", "-p", commit, unified=unified)).encode(
            "ascii", "ignore"
        )
        for commit in commits
    )


def get_files(repo, commits):
    return [
        {
            "commit_hash": commit,
            "files": [
                {
                    "file_name": file_name,
                    "content": repo.git.show(commit + ":" + file_name),
                }
                for file_name in repo.git.diff_tree(
                    "--no-commit-id", "--name-only", "-r", commit
                ).split("\n")
                if len(file_name)
            ],
        }
        for commit in commits
    ]


def write_archive(destn, commits):
    with ZipFile(destn, "w") as archive:
        for commit in commits:
            for file in commit["files"]:
                archive.writestr(
                    os.path.join(commit["commit_hash"], file["file_name"]),
                    file["content"],
                )


def main():
    parser = ArgumentParser()
    repo = Repo(os.getcwd(), search_parent_directories=True)
    user = parser.user or read_user(repo)
    commits = get_commits(repo, user, parser.after_date, parser.before_date)
    if parser.type == "file":
        write_archive(parser.output, get_files(repo, commits))
    else:
        parser.output.write(get_diffs(repo, commits, parser.unified))
