from pathlib import Path

import fakeredis
import pytest
from flask import Flask

from flask_mailing.utils import DefaultChecker


@pytest.fixture
def default_checker():
    test = DefaultChecker()
    yield test
    del test


@pytest.fixture
@pytest.mark.asyncio
async def redis_checker(scope="redis_config"):
    test = DefaultChecker(db_provider="redis")
    test.redis_client = await fakeredis.aioredis.create_redis_pool(encoding="UTF-8")
    await test.init_redis()
    yield test
    await test.redis_client.flushall()
    await test.close_connections()


@pytest.fixture(autouse=True)
def mail_config():
    home: Path = Path(__file__).parent.parent
    html = home / "files"
    env = {
        "MAIL_USERNAME": "example@test.com",
        "MAIL_PASSWORD": "strong",
        "MAIL_FROM": "example@test.com",
        "MAIL_FROM_NAME": "example",
        "MAIL_PORT": 25,
        "MAIL_SERVER": "localhost",
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": False,
        "MAIL_DEBUG": 0,
        "SUPPRESS_SEND": 1,
        "USE_CREDENTIALS": False,
        "VALIDATE_CERTS": False,
        "MAIL_TEMPLATE_FOLDER": html,
    }

    return env


@pytest.fixture(autouse=True)
def app(mail_config) -> "Flask":
    app = Flask("test_app")
    app.secret_key = "top-secret-key"
    app.testing = True
    app.config.update(mail_config)
    return app
