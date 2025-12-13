from playwright.sync_api import Page
import allure
from databases.spend_db import SpendDb
from tools.logger import get_logger

logger = get_logger("TOOLS HELPER")


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
