from unicodedata import normalize


class Collector(object):
    def __init__(self, repository, user, after, before, unified):
        commits = self.__collect_commits(repository, user, after, before)
        self._artifacts = self.__collect_artifacts(repository, commits, unified)

    @staticmethod
    def __collect_commits(repository, user, after, before):
        commits = repository.git.log(
            "--all", "--reverse", format="%H", author=user, after=after, before=before
        ).split("\n")
        if "" in commits:
            commits.remove("")
        return commits

    @staticmethod
    def __collect_artifacts(repository, commits, unified):
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

        def collect_diff(repository, commit, unified):
            return normalize(
                "NFKD", repository.git.show(commit, "-w", "-p", unified=unified)
            ).encode("ascii", "ignore")

        return [
            {
                "commit_hash": commit,
                "files": collect_files(repository, commit),
                "diff": collect_diff(repository, commit, unified),
            }
            for commit in commits
        ]

    @property
    def Artifacts(self):
        return self._artifacts
