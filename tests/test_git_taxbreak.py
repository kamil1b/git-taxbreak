import pkg_resources

from git_taxbreak import __version__


def test_version():
    assert __version__ == pkg_resources.get_distribution("git_taxbreak").version
