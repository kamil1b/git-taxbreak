import datetime
import sys

import pytest

from git_taxbreak.modules.argument_parser import ArgumentParser


FAKE_TIME = datetime.datetime(year=2018, month=10, day=11)


@pytest.fixture
def patch_datetime_today(monkeypatch):
    class DateTimeMock(datetime.datetime):
        @classmethod
        def today(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, "datetime", DateTimeMock)


def test_user_parser():
    user = "Tom"
    sys.argv = ["", "--user=" + user]
    parser = ArgumentParser()
    assert user == parser.user


@pytest.mark.parametrize("type", ["diff", "file"])
def test_type_parser(type):
    sys.argv = ["", "--type=" + type]
    parser = ArgumentParser()
    assert type == parser.type


def test_output_parser(tmp_path):
    filename = tmp_path / "file.zip"
    filename.touch()
    sys.argv = ["", "--output=" + str(filename)]
    parser = ArgumentParser()
    assert parser.output == str(filename)


def test_output_incorrect_argument(tmp_path):
    filename = tmp_path / "file.zip"
    filename.touch(mode=0o400)
    sys.argv = ["", "--output=" + str(filename)]
    with pytest.raises(SystemExit):
        ArgumentParser()


def test_valid_date_default_value(patch_datetime_today):
    sys.argv = [""]
    parser = ArgumentParser()
    assert str(parser.before_date) == FAKE_TIME.strftime("%m/%d/%y")
    assert str(parser.after_date) == FAKE_TIME.strftime("%m/1/%y")


def test_date_parser():
    sys.argv = [
        "",
        "--before=" + FAKE_TIME.strftime("%m/%d/%y"),
        "--after=" + FAKE_TIME.strftime("%m/1/%y"),
    ]
    parser = ArgumentParser()
    assert str(parser.before_date) == FAKE_TIME.strftime("%m/%d/%y")
    assert str(parser.after_date)


def test_unified_parser():
    sys.argv = ["", "--unified=1"]
    parser = ArgumentParser()
    assert parser.unified == 1
