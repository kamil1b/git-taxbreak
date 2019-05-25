from git_taxbreak.modules.writter import Writter


class DummyOutput(object):
    def write(self, output):
        self.result = output


def test_diff():
    diffs = ["diff1", "diff2", "diff3"]
    artifacts = [{"diff": diff} for diff in diffs]
    dummy_output = DummyOutput()
    expected_diff = str("\n\n").join(diffs)
    Writter.diff(artifacts, dummy_output.write)
    assert dummy_output.result == expected_diff


def test_zip():
    pass
