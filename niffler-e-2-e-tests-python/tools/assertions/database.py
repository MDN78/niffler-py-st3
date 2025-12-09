import allure

from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("DATABASE ASSERTIONS")

def check_category_in_db(response, username: str, test_category: str):
    """Метод проверки категории созданой через UI в базе данных"""
    step = f'Checking that {username} category {test_category} in database'
    with allure.step(step):
        logger.info(step)
        first_category = response[0]
        assert_equal(first_category.username, username, "username")
        assert_equal(first_category.name, test_category, "test_category")


def check_spend_in_db(response, amount: float, category_name: str, description: str, username: str):
    """Метод проверки наличие созданной через UI траты в базе данных"""
    step = f'Checking that {username} spends in database'
    with allure.step(step):
        for spend, category in response:
            logger.info(step)
            assert_equal(username, spend.username, "username")
            assert_equal(description, spend.description, "description")
            assert_equal(amount, spend.amount, "amount")
            assert_equal(category_name, category_name, "category_name")
