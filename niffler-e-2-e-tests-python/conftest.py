import os

import json

import pytest
from dotenv import load_dotenv

from clients.spends_client import SpendsHttpClient
from clients.category_client import CategoryHttpClient
from databases.spend_db import SpendDb
from models.category import CategoryAdd
from models.config import Envs

from playwright.sync_api import Page
from app.pages.auth_page import AuthPage
from playwright.sync_api import Browser
from app.pages.profile_page import ProfilePage
from app.pages.spend_page import SpendPage


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


@pytest.fixture(scope='session')
def spends_client(envs, get_token_from_user_state) -> SpendsHttpClient:
    """
    Метод возвращения instance класса SpendsHttpClient
    :param envs: загрузка данный с env файла
    :param get_token_from_user_state: аутентификация пользователя
    :return: instance класса SpendsHttpClient
    """
    return SpendsHttpClient(envs.gateway_url, get_token_from_user_state)


@pytest.fixture(scope='session')
def category_client(envs, get_token_from_user_state) -> CategoryHttpClient:
    """
    Метод возвращения instance класса CategoryHttpClient
    :param envs: загрузка данный с env файла
    :param get_token_from_user_state: аутентификация пользователя
    :return: instance  класса CategoryHttpClient
    """
    return CategoryHttpClient(envs.gateway_url, get_token_from_user_state)


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    """
    Метод возвращения instance класса SpendDb
    :param envs: загрузка данный с env файла
    :param auth: аутентификация пользователя
    :return: instance класса SpendDb
    """
    return SpendDb(envs.spend_db_url)


@pytest.fixture(params=[])
def category(request, category_client: CategoryHttpClient, spend_db: SpendDb):
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
def category_db(request, category_client: CategoryHttpClient, spend_db: SpendDb):
    category = category_client.add_category(request.param)
    yield category
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request, spends_client: SpendsHttpClient):
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


@pytest.fixture(scope="session")
def auth_storage(tmp_path_factory):
    return tmp_path_factory.mktemp("session") / "niffler_user.json"


@pytest.fixture(scope="session")
def initialize_browser_state(browser: Browser, envs, auth_storage):
    context = browser.new_context()
    page = context.new_page()

    registration_page = AuthPage(page=page)
    registration_page.visit(envs.frontend_url)
    registration_page.login(username=envs.test_username, password=envs.test_password)
    registration_page.spending_title_exists("History of Spendings")

    context.storage_state(path=auth_storage)
    print(f"Auth state saved to: {auth_storage}")
    context.close()

    return auth_storage


@pytest.fixture(scope="function")
def chromium_page_with_state(browser: Browser, initialize_browser_state):
    """Страница с предустановленной авторизацией"""
    context = browser.new_context(storage_state=initialize_browser_state)
    page = context.new_page()

    yield page

    context.close()


@pytest.fixture(scope="function")
def spends_page(chromium_page_with_state: Page) -> SpendPage:
    return SpendPage(chromium_page_with_state)


@pytest.fixture(scope="function")
def spends_page_late(chromium_page_with_state: Page, category, spends) -> SpendPage:
    return SpendPage(chromium_page_with_state)


@pytest.fixture()
def open_spend_page(spends_page, envs):
    spends_page.visit(envs.frontend_url)
    spends_page.wait_for_load()
    spends_page.reload()


@pytest.fixture(scope="function")
def profile_page(chromium_page_with_state: Page) -> ProfilePage:
    return ProfilePage(chromium_page_with_state)


@pytest.fixture()
def open_profile_page(profile_page, envs):
    profile_page.visit(envs.profile_url)
    profile_page.wait_for_load()


@pytest.fixture(scope="function")
def login_page(page: Page) -> AuthPage:
    return AuthPage(page)


@pytest.fixture
def open_login_page(login_page, envs):
    login_page.visit(envs.frontend_url)
    login_page.wait_for_load()


@pytest.fixture(scope="session")
def get_token_from_user_state(initialize_browser_state):
    with open(initialize_browser_state) as json_file:
        data = json.load(json_file)
        api_token = data['origins'][0]['localStorage'][3]['value']
    return api_token
