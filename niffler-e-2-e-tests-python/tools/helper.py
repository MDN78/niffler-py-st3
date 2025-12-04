from playwright.sync_api import Page
import allure

from databases.spend_db import SpendDb
from tools.logger import get_logger

logger = get_logger("TOOLS HELPER")


def check_category_in_db(response, username: str, test_category: str):
    """Метод проверки категории созданой через UI в базе данных"""
    step = f'Checking that {username} category {test_category} in database'
    with allure.step(step):
        logger.info(step)
        first_category = response[0]
        assert first_category.username == username
        assert first_category.name == test_category


def check_spend_in_db(response, amount: float, category_name: str, description: str, username: str):
    """Метод проверки наличие созданной через UI траты в базе данных"""
    step = f'Checking that {username} spends in database'
    with allure.step(step):
        for spend, category in response:
            logger.info(step)
            assert description == spend.description
            assert username == spend.username
            assert amount == spend.amount
            assert category_name == category.name


@allure.step('DB. Delete category from database')
def delete_category_in_db(response, spend_db: SpendDb):
    """Метод удаления категории из базы данных"""
    for item in response:
        spend_sql_obj = item[0]
        category_id = spend_sql_obj.category_id
        spend_db.delete_category(category_id)


def delete_spend_after_action(username: str, spend_db: SpendDb):
    """Метод удаления траты после действия теста"""
    step = f'Delete {username} spends in database'
    with allure.step(step):
        logger.info(step)
        spend_db.delete_spends_by_user(username)


def mock_static_resources(page: Page):
    """
    Метод отключения подгрузки статических файлов
    """
    page.route("**/*.{ico,png,jpg,webp,mp3,mp4,woff,woff2}", lambda route: route.abort())
