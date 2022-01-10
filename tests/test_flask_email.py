from flask_mailing.config import ConnectionConfig


def test_configuration(mail_config):
    conf = ConnectionConfig.parse_obj(mail_config)
    assert conf.MAIL_USERNAME == "example@test.com"
    assert conf.MAIL_PORT == 25
