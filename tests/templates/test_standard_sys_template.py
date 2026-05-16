from enums.StandardErrEnum import StandardSysErrEnum
from templates.StandardSysTemplate import StandardLogDataTemplate


def test_standard_log_data_keeps_plain_code_and_message():
    data = StandardLogDataTemplate(code=1234, msg="custom message")

    assert data.code == 1234
    assert data.msg == "custom message"


def test_standard_log_data_info_returns_copy():
    data = StandardLogDataTemplate(code=1234, msg="custom message")

    info = data.info
    info["msg"] = "changed"

    assert data.msg == "custom message"
    assert info == {"code": 1234, "msg": "changed"}


def test_standard_log_data_converts_enum_to_code_and_message():
    data = StandardLogDataTemplate(code=StandardSysErrEnum.IOFAIL, msg="ignored")

    assert data.code == 5002
    assert data.msg == "IO错误"
    assert data.info == {"code": 5002, "msg": "IO错误"}
