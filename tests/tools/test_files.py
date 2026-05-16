from datetime import datetime

import pytest

import tools.Files as files_module
from tools.Files import create_dir, create_file


class FixedDateTime(datetime):
    @classmethod
    def now(cls):
        return cls(2026, 5, 14, 12, 34, 56)


def test_create_dir_creates_directory_without_date(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = create_dir("sample")

    assert result == tmp_path.joinpath("sample").as_posix()
    assert tmp_path.joinpath("sample").is_dir()


def test_create_dir_creates_directory_with_date_suffix(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(files_module, "datetime", FixedDateTime)

    result = create_dir("sample", need_date=True)

    expected = tmp_path.joinpath("sample", "20260514")
    assert result == expected.as_posix()
    assert expected.is_dir()


def test_create_dir_raises_for_empty_directory_name():
    with pytest.raises(ValueError, match=r"参数\[dir_name\]不能为空"):
        create_dir("")


def test_create_dir_wraps_internal_errors(monkeypatch):
    class BrokenPath:
        def joinpath(self, _):
            raise OSError("boom")

    monkeypatch.setattr(files_module.Path, "cwd", lambda: BrokenPath())

    with pytest.raises(Exception, match="创建目录失败"):
        create_dir("sample")


def test_create_file_creates_file_without_second_suffix(tmp_path):
    result = create_file(tmp_path.as_posix(), "report", ".txt")

    expected = tmp_path.joinpath("report.txt")
    assert result == expected.as_posix()
    assert expected.is_file()


def test_create_file_creates_file_with_second_suffix(tmp_path, monkeypatch):
    monkeypatch.setattr(files_module, "datetime", FixedDateTime)

    result = create_file(tmp_path.as_posix(), "report", ".txt", is_second=True)

    expected = tmp_path.joinpath("report123456.txt")
    assert result == expected.as_posix()
    assert expected.is_file()


def test_create_file_raises_for_missing_parameters(tmp_path):
    with pytest.raises(ValueError, match=r"参数\[op_path, op_file_name, op_end_with\]不能为空"):
        create_file(tmp_path.as_posix(), "", ".txt")


def test_create_file_raises_when_path_is_not_directory(tmp_path):
    file_path = tmp_path.joinpath("not_a_dir.txt")
    file_path.write_text("content", encoding="utf-8")

    with pytest.raises(ValueError, match=r"参数\[op_path\]指定的目录不存在或不是一个目录"):
        create_file(file_path.as_posix(), "report", ".txt")


def test_create_file_wraps_internal_errors(tmp_path, monkeypatch):
    def broken_touch(self):
        raise OSError("boom")

    monkeypatch.setattr(files_module.Path, "touch", broken_touch)

    with pytest.raises(Exception, match="创建文件失败"):
        create_file(tmp_path.as_posix(), "report", ".txt")
