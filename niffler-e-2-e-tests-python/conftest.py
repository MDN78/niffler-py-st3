import os
import allure
import json

import pytest
from _pytest.fixtures import SubRequest
from pytest import Item, FixtureDef, FixtureRequest
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
from tools.allure.reportet import allure_reporter, allure_logger
from tools.allure.environment import create_allure_environment_file
from tools.helper import mock_static_resources


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown(item):
    yield
    reporter = allure_reporter(item.config)
    test = reporter.get_test(None)
    test.labels = list(
        filter(lambda x: not (x.name == "tag" and "@pytest.mark.usefixtures" in x.value),
               test.labels)
    )


@pytest.fixture(scope='session', autouse=True)
def save_allure_environment_file():
    """ Метод сохранения окружения в файл для allure отчета"""
    yield
    create_allure_environment_file()


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
def spends_client(envs: Envs, get_token_from_user_state) -> SpendsHttpClient:
    """
    Метод возвращения instance класса SpendsHttpClient
    :param envs: загрузка данный с env файла
    :param get_token_from_user_state: аутентификация пользователя
    :return: instance класса SpendsHttpClient
    """
    return SpendsHttpClient(envs.gateway_url, get_token_from_user_state)


@pytest.fixture(scope='session')
def category_client(envs: Envs, get_token_from_user_state) -> CategoryHttpClient:
    """
    Метод возвращения instance класса CategoryHttpClient
    :param envs: загрузка данный с env файла
    :param get_token_from_user_state: аутентификация пользователя
    :return: instance  класса CategoryHttpClient
    """
    return CategoryHttpClient(envs.gateway_url, get_token_from_user_state)


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
    all_spends = spends_client.get_spends()
    if t_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([t_spend.id])


@pytest.fixture(scope="session")
def auth_storage(tmp_path_factory):
    return tmp_path_factory.mktemp("session") / "niffler_user.json"


@pytest.fixture(scope="session")
def initialize_browser_state(browser: Browser, envs: Envs, auth_storage):
    """Метод получение аутентификационного токена"""
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


@pytest.fixture
def chromium_page_with_state(browser: Browser, initialize_browser_state, request: SubRequest):
    """Страница с предустановленной авторизацией"""
    context = browser.new_context(storage_state=initialize_browser_state)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    mock_static_resources(page)

    yield page

    context.tracing.stop(path=f'./tracing/{request.node.name}.zip')
    context.close()
    allure.attach.file(f'./tracing/{request.node.name}.zip', name='trace', extension='zip')


@pytest.fixture
def spends_page(chromium_page_with_state: Page) -> SpendPage:
    """Метод возвращения instance класса SpendPage"""
    return SpendPage(chromium_page_with_state)


@pytest.fixture
def spends_page_late(chromium_page_with_state: Page, category, spends) -> SpendPage:
    """Метод возвращения instance класса SpendPage with category and spends"""
    return SpendPage(chromium_page_with_state)


@pytest.fixture
def open_spend_page(spends_page: SpendPage, envs: Envs):
    spends_page.visit(envs.frontend_url)
    spends_page.wait_for_load()
    spends_page.reload()


@pytest.fixture
def profile_page(chromium_page_with_state: Page) -> ProfilePage:
    """Метод возвращения instance класса ProfilePage"""
    return ProfilePage(chromium_page_with_state)


@pytest.fixture
def open_profile_page(profile_page: ProfilePage, envs):
    profile_page.visit(envs.profile_url)
    profile_page.wait_for_load()


@pytest.fixture
def login_page(page: Page) -> AuthPage:
    """Метод возвращения instance класса AuthPage"""
    return AuthPage(page)


@pytest.fixture
def open_login_page(login_page: AuthPage, envs):
    login_page.visit(envs.frontend_url)
    login_page.wait_for_load()


@pytest.fixture(scope="session")
def get_token_from_user_state(initialize_browser_state):
    """Метод получения аутентификационного токена с файла из временного хранилища"""
    with open(initialize_browser_state) as json_file:
        data = json.load(json_file)
        api_token = data['origins'][0]['localStorage'][3]['value']
    return api_token
