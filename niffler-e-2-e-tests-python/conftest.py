import os
import time

import pytest
from dotenv import load_dotenv
from selene import browser

from clients.spends_client import SpendsHttpClient


@pytest.fixture(scope="session", autouse=True)
def envs():
    """Загрузка файла .env"""
    load_dotenv()


@pytest.fixture(scope="session")
def frontend_url(envs):
    """Получение url приложения: http://frontend.niffler.dc """
    return os.getenv("FRONTEND_URL")


@pytest.fixture(scope="session")
def gateway_url(envs):
    """Получение url приложения"""
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def profile_url(envs):
    """Получение url приложения"""
    return os.getenv("PROFILE_URL")


@pytest.fixture(scope="session")
def registration_url(envs):
    return os.getenv("REGISTRATION_URL")


@pytest.fixture(scope="session")
def app_user(envs):
    """Данные пользователя из файла .env"""
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


@pytest.fixture(scope='session')
def auth(frontend_url, app_user) -> str:
    """
    Фикстура аутентификации пользователя посредством UI интерфейса
    :param frontend_url: url приложения http://frontend.niffler.dc
    :param app_user: заранее созданный пользователь
    :return: авторизационный id_token
    """
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    time.sleep(1)
    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope='session')
def spends_client(gateway_url, auth) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, auth)


@pytest.fixture(params=[])
def category(request, spends_client: SpendsHttpClient) -> str:
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category["name"] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)
    return category_name


@pytest.fixture(params=[])
def spends(request, spends_client: SpendsHttpClient):
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spends = spends_client.get_spends()
    if spend["id"] in [spend["id"] for spend in all_spends]:
        spends_client.remove_spends([spend["id"]])


@pytest.fixture()
def delete_spends(auth, spends_client):
    """Удаление Траты после теста"""
    yield
    response = spends_client.get_spends()
    spends_client.remove_spends(response[0]["id"])


@pytest.fixture()
def main_page(auth, frontend_url):
    """ Фикстура открывает главную страницу с аутентифицированным пользователем"""
    browser.open(frontend_url)


@pytest.fixture()
def main_page_late(category, spends, frontend_url):
    browser.open(frontend_url)


@pytest.fixture()
def profile_page(auth, profile_url):
    """Открытие страницы профиля аутентифицированного пользователя"""
    browser.open(profile_url)


@pytest.fixture()
def login_page(frontend_url):
    browser.open(frontend_url)
    yield
    browser.quit()
