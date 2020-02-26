import git
import pytest
from git_taxbreak import cmd

EMPTY_CONFIG = {}
TEST_USER = "TEST_USER"
CORRECT_CONFIG = {
    "user": {"dummy_entry": "value1", "dummy_entry2": "value2", "name": TEST_USER}
}
CONFIG_WITHOUT_USER = {"user": {"dummy_entry": "value1", "dummy_entry2": "value2"}}


class DummyReader(object):
    class DummyIter:
        def __init__(self, values):
            self.values = values

        def __iter__(self):
            return self

        def next(self):
            return self.__next__()

        def __next__(self):
            if not self.values:
                raise StopIteration
            return self.values.popitem()

    def __init__(self, config):
        self._config = config

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def sections(self):
        return self._config.keys()

    def items(self, key):
        return self.DummyIter(self._config[key])


@pytest.fixture
def patch_config_reader(monkeypatch, config):
    class RepoMock(git.Repo):
        @classmethod
        def config_reader(cls):
            return DummyReader(config)

    monkeypatch.setattr(git, "Repo", RepoMock)


@pytest.mark.parametrize(
    "config, user",
    [[EMPTY_CONFIG, None], [CONFIG_WITHOUT_USER, None], [CORRECT_CONFIG, TEST_USER]],
)
def test_read_user_user(patch_config_reader, user):
    assert cmd.read_user(git.Repo) is user
