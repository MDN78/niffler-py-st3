import allure
import pytest

from _pytest.fixtures import FixtureRequest
from clients.category_client import CategoryHttpClient
from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from models.category import CategoryAdd
from models.config import Envs

from tools.logger import get_logger

logger = get_logger("FIXTURES")


@pytest.fixture(scope='session')
def spends_client(envs: Envs, get_token_from_user_state) -> SpendsHttpClient:
    """
    Метод возвращения instance класса SpendsHttpClient
    :param envs: загрузка данный с env файла
    :param get_token_from_user_state: аутентификация пользователя
    :return: instance класса SpendsHttpClient
    """
    return SpendsHttpClient(envs, get_token_from_user_state)


@pytest.fixture(scope='session')
def category_client(envs: Envs, get_token_from_user_state) -> CategoryHttpClient:
    """
    Метод возвращения instance класса CategoryHttpClient
    :param envs: загрузка данный с env файла
    :param get_token_from_user_state: аутентификация пользователя
    :return: instance  класса CategoryHttpClient
    """
    return CategoryHttpClient(envs, get_token_from_user_state)


@pytest.fixture(scope="session")
def spend_db(envs: Envs) -> SpendDb:
    """
    Метод возвращения instance класса SpendDb
    :param envs: загрузка данный с env файла
    :param auth: аутентификация пользователя
    :return: instance класса SpendDb
    """
    return SpendDb(envs.spend_db_url)


@pytest.fixture(params=[])
def category(request: FixtureRequest, category_client: CategoryHttpClient, spend_db: SpendDb):
    """
    Метод добавления категории через CategoryHttpClient
    :param request: получение наименования категории
    :param category_client: осуществляет запросы на CategoryHttpClient
    :param spend_db
    """
    category_name = request.param
    category = category_client.add_category(CategoryAdd(name=category_name))
    yield category.name
    with allure.step('DB. Delete category'):
        spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def category_db(request, category_client: CategoryHttpClient, spend_db: SpendDb):
    """Фмкстура создания категории в базе данных и удаление после теста"""
    category = category_client.add_category(request.param)
    yield category
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request: FixtureRequest, spends_client: SpendsHttpClient):
    """
    Метод добавления Траты и удаление после теста
    :param request: получение параметров Траты
    :param spends_client: осуществление запросов через SpendsHttpClient
    """
    t_spend = spends_client.add_spends(request.param)
    yield t_spend
    with allure.step('HTTP client. Delete spends'):
        logger.info(f'Delete spend')
        all_spends = spends_client.get_spends()
        if t_spend.id in [spend.id for spend in all_spends]:
            spends_client.remove_spends([t_spend.id])
