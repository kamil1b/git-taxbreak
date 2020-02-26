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


@pytest.fixture
def default_output(monkeypatch, tmp_path):
    patched = tmp_path / "default.zip"
    monkeypatch.setattr("git_taxbreak.modules.argument_parser.DEFAULT_OUTPUT", patched)
    return patched


def test_user_parser(default_output):
    user = "Tom"
    sys.argv = ["", "--user=" + user]
    parser = ArgumentParser()
    assert user == parser.user


def test_default_output(default_output):
    sys.argv = [""]
    parser = ArgumentParser()
    assert str(parser.output) == str(default_output)


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


def test_valid_date_default_value(patch_datetime_today, default_output):
    sys.argv = [""]
    parser = ArgumentParser()
    assert str(parser.before_date) == FAKE_TIME.strftime("%m/%d/%y")
    assert str(parser.after_date) == FAKE_TIME.strftime("%m/1/%y")


def test_date_parser(default_output):
    sys.argv = [
        "",
        "--before=" + FAKE_TIME.strftime("%m/%d/%y"),
        "--after=" + FAKE_TIME.strftime("%m/1/%y"),
    ]
    parser = ArgumentParser()
    assert str(parser.before_date) == FAKE_TIME.strftime("%m/%d/%y")
    assert str(parser.after_date)


def test_date_parser_thow_on_incorrect_date(default_output):
    sys.argv = ["", "--before=" + "incorrect_date"]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ArgumentParser()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def test_unified_parser(default_output):
    sys.argv = ["", "--unified=1"]
    parser = ArgumentParser()
    assert parser.unified == 1
