""" Module provide functionality for save collected artifacts
@author Kamil Luczak
"""
import zipfile
from os import path


class Writter:
    """Class response for save artifacts to zip file"""

    def __init__(self, destn):
        self.__archive = zipfile.ZipFile(destn, "w")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__archive.close()

    def archive(self, artifacts):
        def append_commit_to_archive(commit, archive):
            commit_hash = commit["commit_hash"]
            archive.writestr(path.join(commit_hash, "diff.txt"), commit["diff"])
            for file in commit["files"]:
                if file["content"]:
                    archive.writestr(
                        path.join(commit_hash, file["file_name"]), file["content"]
                    )

        for commit in artifacts:
            append_commit_to_archive(commit, self.__archive)
