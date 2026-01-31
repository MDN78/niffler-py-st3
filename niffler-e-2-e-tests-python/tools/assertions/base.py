import allure
from typing import Any, Sized
from tools.logger import get_logger

logger = get_logger("BASE ASSERTIONS")


@allure.step("Check that response status code equals to {expected}")
def assert_status_code(actual: int, expected: int):
    """
    Проверяет, что фактический статус-код ответа соответствует ожидаемому.

    :param actual: Фактический статус-код ответа.
    :param expected: Ожидаемый статус-код.
    :raises AssertionError: Если статус-коды не совпадают.
    """
    logger.info(f"Check that response status code equals to {expected}")
    assert actual == expected, (
        'Incorrect response status code. '
        f'Expected status code: {expected}. '
        f'Actual status code: {actual}'
    )


@allure.step("Check that {name} equals to {expected}")
def assert_equal(actual: Any, expected: Any, name: str):
    """
    Проверяет, что фактическое значение равно ожидаемому.

    :param name: Название проверяемого значения.
    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение.
    :raises AssertionError: Если фактическое значение не равно ожидаемому.
    """
    logger.info(f'Check that "{name}" equals to {expected}')
    assert actual == expected, (
        f'Incorrect value: "{name}". '
        f'Expected value: {expected}. '
        f'Actual value: {actual}'
    )


@allure.step("Check that {name} unequals to {expected}")
def assert_unequal(actual: Any, expected: Any, name: str):
    """
    Проверяет, что фактическое значение не равно ожидаемому.

    :param name: Название проверяемого значения.
    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение.
    :raises AssertionError: Если фактическое значение не равно ожидаемому.
    """
    logger.info(f'Check that "{name}" unequals to zero')
    assert actual != expected, (
        f'Incorrect value: "{name}". '
        f'Expected value: {expected}. '
        f'Actual value: {actual}'
    )


@allure.step("Check length objects")
def assert_length(actual: Sized, expected: Sized, name: str):
    """
    Проверяет, что длины двух объектов совпадают.

    :param name: Название проверяемого объекта.
    :param actual: Фактический объект.
    :param expected: Ожидаемый объект.
    :raises AssertionError: Если длины не совпадают.
    """
    with allure.step(f"Check that length of {name} equals to {len(expected)}"):
        logger.info(f'Check that length of "{name}" equals to {len(expected)}')
        assert len(actual) == len(expected), (
            f'Incorrect object length: "{name}". '
            f'Expected length: {len(expected)}. '
            f'Actual length: {len(actual)}'
        )


@allure.step("Check that actual dates greater than zero")
def assert_greater_than_zero(actual: Any, name: str):
    """
    Проверяет, что фактическое значение больше нуля.

    :param name: Название проверяемого значения.
    :param actual: Фактическое значение.
    :raises AssertionError: Если значение не больше нуля.
    """
    logger.info(f'Check that "{name}" is greater than 0')
    assert actual > 0, (
        f'Incorrect value: "{name}". '
        f'Expected: greater than 0. '
        f'Actual value: {actual}'
    )


@allure.step("Check that {name} exists")
def assert_exists(dates: Any, name: str):
    logger.info(f'Check that "{name}" exists')
    assert dates, (
        f'Incorrect value: "{dates}". '
        f'Expected value: {dates}. '
        f'Actual value: {dates}'
    )


@allure.step("Check that {name} non exists")
def assert_non_exists(dates: Any, name: str):
    logger.info(f'Check that "{name}" non exists')
    assert not dates, (
        f'Incorrect value: "{dates}". '
        f'Expected value: {dates}. '
        f'Actual value: {dates}'
    )
