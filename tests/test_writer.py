import zipfile

import pytest
from git_taxbreak.modules.writer import Writer


@pytest.fixture
def patch_zip_file(monkeypatch):
    class ZipFileMock(zipfile.ZipFile):
        def __init__(self, *args, **kwargs):
            self.output = args[0]
            self.content = []

        def __enter__(self):
            return self

        def close(self):
            self.output.content = self.content

        def writestr(self, *args, **kwargs):
            file = args[0]
            content = args[1]
            self.content.append({"file_name": file, "content": content})

    monkeypatch.setattr(zipfile, "ZipFile", ZipFileMock)


class DummyOutput:
    content = None


def test_archive_save(patch_zip_file):
    ARTIFACTS = [
        {
            "diff": "diff_content1",
            "message": "summary1\n\nMore text1",
            "commit_hash": "hash1",
            "files": [
                {"file_name": "some_path/file_name1.txt", "content": "file_content1"},
                {"file_name": "some_path2/file_name2.txt", "content": "file_content2"},
                {"file_name": "file_name3.txt", "content": "file_content3"},
            ],
        },
        {
            "diff": "diff_content2",
            "message": "summary2\n\nMore text2",
            "commit_hash": "hash2",
            "files": [
                {"file_name": "some_path/file_name4.txt", "content": "file_content4"},
                {"file_name": "file_name5.txt", "content": "file_content5"},
            ],
        },
    ]

    EXPECTED_CONTENT = [
        {"file_name": "hash1/diff.txt", "content": "diff_content1"},
        {"file_name": "hash1/some_path/file_name1.txt", "content": "file_content1"},
        {"file_name": "hash1/some_path2/file_name2.txt", "content": "file_content2"},
        {"file_name": "hash1/file_name3.txt", "content": "file_content3"},
        {"file_name": "hash2/diff.txt", "content": "diff_content2"},
        {"file_name": "hash2/some_path/file_name4.txt", "content": "file_content4"},
        {"file_name": "hash2/file_name5.txt", "content": "file_content5"},
        {"file_name": "work-commits.txt", "content": "hash1 summary1\nhash2 summary2"},
    ]
    dummy_output = DummyOutput()

    with Writer(dummy_output) as writer:
        writer.archive(ARTIFACTS)
    assert dummy_output.content == EXPECTED_CONTENT


def test_archive_not_throw_when_file_content_not_exist(patch_zip_file):
    ARTIFACTS = [
        {
            "diff": "diff_content1",
            "message": "summary1\n\nMore text1",
            "commit_hash": "hash1",
            "files": [{"file_name": "some_path/file_name1.txt", "content": None}],
        }
    ]

    EXPECTED_CONTENT = [
        {"file_name": "hash1/diff.txt", "content": "diff_content1"},
        {"file_name": "work-commits.txt", "content": "hash1 summary1"},
    ]
    dummy_output = DummyOutput()

    with Writer(dummy_output) as writer:
        writer.archive(ARTIFACTS)
    assert dummy_output.content == EXPECTED_CONTENT
