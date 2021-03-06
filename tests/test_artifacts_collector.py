from git_taxbreak.modules.artifacts_collector import Collector

AUTHOR = "test_author"
DATE_AFTER = ""
DATE_BEFORE = ""


class GitMock(object):
    def __init__(
        self, output, expected_author, expected_before_date, expected_after_date
    ):
        self.output = output
        self.expected_author = expected_author
        self.expected_before_date = expected_before_date
        self.expected_after_date = expected_after_date

    def log(self, *args, **kwargs):
        assert kwargs["author"] == self.expected_author
        assert kwargs["after"] == self.expected_after_date
        assert kwargs["before"] == self.expected_before_date
        return self.output[0]

    def show(self, *args, **kwargs):
        assert args[0] in self.output[2]
        return self.output[2][args[0]]

    def diff_tree(self, *args, **kwargs):
        assert args[3] in self.output[1]
        return self.output[1][args[3]]


class Commit(object):
    def __init__(self, message):
        self.message = message


class RepositoryMock(object):
    def __init__(self, git, commits):
        self.git = git
        self.commits = commits

    def commit(self, commit_hash):
        assert commit_hash in self.commits
        return self.commits[commit_hash]


def test_collector():
    LOG_OUTPUT = "8b8d0dcdf0a81375e8c9b31aaebe4d6c536fdf25\n659a484f0d84f807ceb34bd4f93ac394d23990cb\n"
    DIFF_TREE_OUTPUT = {
        "8b8d0dcdf0a81375e8c9b31aaebe4d6c536fdf25": "A\tfile1\nM\tpath2/file2\nD\tpath3/file3",
        "659a484f0d84f807ceb34bd4f93ac394d23990cb": "A\tfile1\nD\tpath5/file5",
    }
    SHOW_OUTPUT = {
        "8b8d0dcdf0a81375e8c9b31aaebe4d6c536fdf25": "diff1",
        "8b8d0dcdf0a81375e8c9b31aaebe4d6c536fdf25:file1": "output1",
        "8b8d0dcdf0a81375e8c9b31aaebe4d6c536fdf25:path2/file2": "output2",
        "659a484f0d84f807ceb34bd4f93ac394d23990cb": "diff2",
        "659a484f0d84f807ceb34bd4f93ac394d23990cb:file1": "output3",
    }
    git = GitMock(
        [LOG_OUTPUT, DIFF_TREE_OUTPUT, SHOW_OUTPUT], AUTHOR, DATE_BEFORE, DATE_AFTER
    )
    COMMITS = {
        "8b8d0dcdf0a81375e8c9b31aaebe4d6c536fdf25": Commit("message1"),
        "659a484f0d84f807ceb34bd4f93ac394d23990cb": Commit("message2"),
    }
    repo = RepositoryMock(git, COMMITS)

    artifacts = Collector(repo, AUTHOR, DATE_AFTER, DATE_BEFORE).artifacts
    assert artifacts == [
        {
            "commit_hash": "8b8d0dcdf0a81375e8c9b31aaebe4d6c536fdf25",
            "message": "message1",
            "files": [
                {"file_name": "file1", "content": "output1"},
                {"file_name": "path2/file2", "content": "output2"},
                {"file_name": "path3/file3", "content": None},
            ],
            "diff": b"diff1",
        },
        {
            "commit_hash": "659a484f0d84f807ceb34bd4f93ac394d23990cb",
            "message": "message2",
            "files": [
                {"file_name": "file1", "content": "output3"},
                {"file_name": "path5/file5", "content": None},
            ],
            "diff": b"diff2",
        },
    ]
