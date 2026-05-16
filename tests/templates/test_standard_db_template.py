from templates.StandardDBTemplate import TbUserTemplate


def test_tb_user_template_keeps_input_fields():
    user = TbUserTemplate(
        uid="u-1",
        username="tester",
        phone="13800000000",
        password="secret",
    )

    assert user.uid == "u-1"
    assert user.username == "tester"
    assert user.phone == "13800000000"
    assert user.password == "secret"


def test_tb_user_template_info_returns_copy():
    user = TbUserTemplate(
        uid="u-1",
        username="tester",
        phone="13800000000",
        password="secret",
    )

    info = user.info
    info["username"] = "changed"

    assert user.username == "tester"
    assert info["username"] == "changed"
