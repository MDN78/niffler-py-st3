from typing import Any

from tools.assertions.base import assert_equal, assert_exists, assert_non_exists
from tools.logger import get_logger

logger = get_logger("SOAP ASSERTIONS")


def assert_userdata(userdata: Any, username: str) -> None:
    """
    Проверяет что фактические данные соответствуют ожидаемым
    :param userdata: ответ SOAP сервиса
    :param username: Имя пользователя
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check correct SOAP response")
    assert_equal(userdata['username'], username, "username in SOAP message")
    assert_exists(userdata['id'], 'users ID')


def assert_unknown_userdata(userdata: Any, username: str) -> None:
    """
    Проверяет что фактические данные соответствуют ожидаемым
    :param userdata: ответ SOAP сервиса
    :param username: Имя неизвестного пользователя
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check SOAP response")
    assert_equal(userdata['username'], username, "username in SOAP message")
    assert_non_exists(userdata['id'], 'users ID')
    assert_non_exists(userdata['fullname'], 'users fullname')
