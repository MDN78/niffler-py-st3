import os
import time

import pytest
from dotenv import load_dotenv
from selene import browser

from clients.spends_client import SpendsHttpClient
from clients.category_client import CategoryHttpClient
from databases.spend_db import SpendDb
from models.category import CategoryAdd
from models.config import Envs
from pages.spend_page import spend_page


@pytest.fixture(scope="session", autouse=True)
def envs() -> Envs:
    """Загрузка файла .env"""
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        registration_url=os.getenv("REGISTRATION_URL"),
        profile_url=os.getenv("PROFILE_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )


@pytest.fixture(scope="session")
def app_user(envs):
    """Данные пользователя из файла .env"""
    return envs.test_username, envs.test_password


@pytest.fixture(scope='session')
def auth(envs) -> str:
    """
    Метод аутентификации пользователя посредством UI интерфейса
    envs.frontend_url: url приложения http://frontend.niffler.dc
    user: заранее созданный пользователь
    :return: авторизационный id_token
    """
    browser.open(envs.frontend_url)
    browser.element('input[name=username]').set_value(envs.test_username)
    browser.element('input[name=password]').set_value(envs.test_password)
    browser.element('button[type=submit]').click()
    time.sleep(1)
    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope='session')
def spends_client(envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture(scope='session')
def category_client(envs, auth) -> CategoryHttpClient:
    return CategoryHttpClient(envs.gateway_url, auth)


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(params=[])
def category(request, category_client, spend_db):
    """
    Метод добавления категории через CategoryHttpClient
    :param request: получение наименования категории
    :param category_client: осуществляет запросы на CategoryHttpClient
    :param spend_db
    """
    category_name = request.param
    category = category_client.add_category(CategoryAdd(name=category_name))
    yield category.name
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def category_db(request, category_client, spend_db):
    category = category_client.add_category(request.param)
    yield category
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request, spends_client):
    """
    Метод добавления Траты и удаление после теста
    :param request: получение параметров Траты
    :param spends_client: осуществление запросов через SpendsHttpClient
    """
    t_spend = spends_client.add_spends(request.param)
    yield t_spend
    all_spends = spends_client.get_spends()
    if t_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([t_spend.id])


@pytest.fixture()
def delete_spend_fx(request, auth, envs):
    name_category = request.param
    yield name_category
    spend_page.delete_spend(name_category)


@pytest.fixture()
def main_page(auth, envs):
    """ Фикстура открывает главную страницу с аутентифицированным пользователем"""
    browser.open(envs.frontend_url)


@pytest.fixture()
def main_page_late(category, spends, envs):
    browser.open(envs.frontend_url)


@pytest.fixture()
def profile_page(auth, envs):
    """Открытие страницы профиля аутентифицированного пользователя"""
    browser.open(envs.profile_url)


@pytest.fixture()
def login_page(envs):
    browser.open(envs.frontend_url)
    yield
    browser.quit()
