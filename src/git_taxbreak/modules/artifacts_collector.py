from unicodedata import normalize


class Collector:
    """Class response for collect artifacts from repository"""

    def __init__(self, repository, user, after, before):
        commits = self.__collect_commits(repository, user, after, before)
        self._artifacts = self.__collect_artifacts(repository, commits)

    @staticmethod
    def __collect_commits(repository, user, after, before):
        commits = repository.git.log(
            "--all", "--reverse", format="%H", author=user, after=after, before=before
        ).split("\n")
        if "" in commits:
            commits.remove("")
        return commits

    @staticmethod
    def __collect_artifacts(repository, commits):
        def collect_files(repository, commit):
            return [
                {
                    "file_name": file_name,
                    "content": repository.git.show(commit + ":" + file_name)
                    if status != "D"
                    else None,
                }
                for status, file_name in map(
                    lambda file_entry: file_entry.split("\t"),
                    repository.git.diff_tree(
                        "--no-commit-id", "--name-status", "-r", commit
                    ).split("\n"),
                )
                if len(file_name)
            ]

        def collect_diff(repository, commit):
            return normalize(
                "NFKD", repository.git.show(commit, "-w", "-p", unified=0)
            ).encode("ascii", "ignore")

        return [
            {
                "commit_hash": commit,
                "message": repository.commit(commit).message,
                "files": collect_files(repository, commit),
                "diff": collect_diff(repository, commit),
            }
            for commit in commits
        ]

    @property
    def artifacts(self):
        return self._artifacts
