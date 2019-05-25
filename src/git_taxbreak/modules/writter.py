from os import path
from zipfile import ZipFile


class Writter:
    @staticmethod
    def archive(destn, artifacts):
        with ZipFile(destn, "w") as archive:
            for commit in artifacts:
                for file in commit["files"]:
                    if file["content"]:
                        archive.writestr(
                            path.join(commit["commit_hash"], file["file_name"]),
                            file["content"],
                        )

    @staticmethod
    def diff(artifacts, output):
        output("\n\n".join(commit["diff"] for commit in artifacts))
