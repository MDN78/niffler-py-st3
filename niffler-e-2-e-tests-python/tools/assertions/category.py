from typing import Any

from models.category import Category
from tools.logger import get_logger
from tools.assertions.base import assert_equal

logger = get_logger("CATEGORY ASSERTIONS")

def assert_category(actual: Category, expected: Any):
    """
    Проверяет, что фактические данные Категории соответствуют ожидаемым.

    :param actual: Фактические данные Категории.
    :param expected: Ожидаемые данные Категории.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check category")
    assert_equal(actual.name, expected, "category name")

