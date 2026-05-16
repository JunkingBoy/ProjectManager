from enums.StandardErrEnum import StandardSysErrEnum


def test_standard_sys_err_enum_values_match_expected_definition():
    assert StandardSysErrEnum.OSFAIL.value == (5001, "操作系统错误")
    assert StandardSysErrEnum.IOFAIL.value == (5002, "IO错误")
    assert StandardSysErrEnum.TYPEFAIL.value == (5003, "类型错误")
    assert StandardSysErrEnum.ATTRIBUTEFAIL.value == (5004, "属性错误")
    assert StandardSysErrEnum.CONNECTFAIL.value == (5005, "连接错误")
    assert StandardSysErrEnum.UNKNOWNFAIL.value == (5006, "未知错误")


def test_standard_sys_err_enum_member_order_is_stable():
    assert [member.name for member in StandardSysErrEnum] == [
        "OSFAIL",
        "IOFAIL",
        "TYPEFAIL",
        "ATTRIBUTEFAIL",
        "CONNECTFAIL",
        "UNKNOWNFAIL",
    ]
