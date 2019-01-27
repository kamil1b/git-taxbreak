from git_taxbreak import __version__
import pkg_resources


def test_version():
    assert __version__ == pkg_resources.get_distribution("git_taxbreak").version
