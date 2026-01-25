import json
from typing import Any

from databases.auth_db import UserDb
from databases.userdata_db import UserdataDb
from tools.assertions.base import assert_equal, assert_unequal
from tools.logger import get_logger

logger = get_logger("KAFKA ASSERTIONS")


def check_message_content(event: Any, username: str):
    """
    Проверяет, что фактические данные соответствуют ожидаемым.

    :param event: Фактические данные.
    :param username: Ожидаемые данные.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    actual = json.loads(event.decode('utf8'))['username']
    logger.info("Check kafka message content")
    assert_equal(actual, username, "kafka content")


def check_that_message_from_kafka_exist(event: Any, expected: Any):
    """
    Проверяет, что сообщение Кафка существует.

    :param event: Фактические данные.
    :param username: Ожидаемые данные.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check that message from kafka exist")
    assert_unequal(event, expected, 'message kafka exist')


def check_new_record_in_auth_db(auth_db: UserDb, username: Any) -> None:
    """
    Проверяет наличие новой записи в базе auth_db.
    """
    record = auth_db.get_user_by_username(username)
    logger.info("Check new record in auth db")
    assert_equal(record, None, "record in auth db")


def check_new_record_in_user_db(user_db: UserdataDb, username: Any) -> None:
    """
    Проверяет наличие новой записи в базе данных user_db.
    """
    user_db = user_db.get_user(username).username
    logger.info("Check new record in userdata db")
    assert_equal(user_db, username, "username in db")
