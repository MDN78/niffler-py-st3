import allure
from typing import Union
from models.spend import SpendAdd, Spend
from tools.logger import get_logger
from tools.assertions.base import assert_equal

logger = get_logger("SPENDS ASSERTIONS")

@allure.step("Check spend")
def assert_spend(actual: Spend, expected: Union[Spend, SpendAdd]):
    """
    Проверяет, что фактические данные траты соответствуют ожидаемым.

    :param actual: Фактические данные траты.
    :param expected: Ожидаемые данные траты.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check spend")
    assert_equal(actual.amount, expected.amount, "amount")
    assert_equal(actual.currency, expected.currency, "currency")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.category.name, expected.category.name, "category")

