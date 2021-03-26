""" Module provide functionality for save collected artifacts
@author Kamil Luczak
"""
import zipfile
from os import path


class Writer:
    """Class response for save artifacts to zip file"""

    def __init__(self, destn):
        self.__archive = zipfile.ZipFile(destn, "w")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__archive.close()

    @staticmethod
    def __append_commit_to_archive(commit, archive):
        commit_hash = commit["commit_hash"]
        archive.writestr(path.join(commit_hash, "diff.txt"), commit["diff"])
        for file in commit["files"]:
            if file["content"]:
                archive.writestr(
                    path.join(commit_hash, file["file_name"]), file["content"]
                )

    @staticmethod
    def __append_summaries_to_commit(summaries, archive):
        archive.writestr("work-commits.txt", "\n".join(summaries))

    def archive(self, artifacts):
        summaries = []
        for commit in artifacts:
            summaries.append(
                (" ").join(
                    [commit["commit_hash"], commit["message"].partition("\n")[0]]
                )
            )
            self.__append_commit_to_archive(commit, self.__archive)
        self.__append_summaries_to_commit(summaries, self.__archive)
