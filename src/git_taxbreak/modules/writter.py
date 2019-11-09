import zipfile
from os import path


class Writter:
    @staticmethod
    def archive(destn, artifacts):
        def append_commit_to_archive(commit, archvie):
            commit_hash = commit["commit_hash"]
            archive.writestr(path.join(commit_hash, "diff.txt"), commit["diff"])
            for file in commit["files"]:
                if file["content"]:
                    archive.writestr(
                        path.join(commit_hash, file["file_name"]), file["content"]
                    )

        with zipfile.ZipFile(destn, "w") as archive:
            for commit in artifacts:
                append_commit_to_archive(commit, archive)
