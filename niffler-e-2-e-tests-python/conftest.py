import os
from pathlib import Path
import json

import pytest
from dotenv import load_dotenv
# from selene import browser, be

from clients.spends_client import SpendsHttpClient
from clients.category_client import CategoryHttpClient
from databases.spend_db import SpendDb
from models.category import CategoryAdd
from models.config import Envs
# from pages.spend_page import spend_page

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
def spends_client(envs, get_token_from_user_state, playwright) -> SpendsHttpClient:
    """
    Метод возвращения instance класса SpendsHttpClient
    :param envs: загрузка данный с env файла
    :param get_token_from_user_state: аутентификация пользователя
    :param playwright
    :return: instance класса SpendsHttpClient
    """
    return SpendsHttpClient(envs.gateway_url, get_token_from_user_state, playwright)


@pytest.fixture(scope='session')
def category_client(envs, get_token_from_user_state, playwright) -> CategoryHttpClient:
    """
    Метод возвращения instance класса CategoryHttpClient
    :param envs: загрузка данный с env файла
    :param get_token_from_user_state: аутентификация пользователя
    :param playwright
    :return: instance  класса CategoryHttpClient
    """
    return CategoryHttpClient(envs.gateway_url, get_token_from_user_state, playwright)


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
def initialize_browser_state(browser: Browser, envs, request):
    """Автоматически создает файл с состоянием авторизации перед всеми тестами"""

    # Получаем корневую директорию проекта
    project_root = Path(request.config.rootdir)

    # Создаем папку auth_data в корне проекта
    auth_dir = project_root / "auth_data"
    auth_dir.mkdir(exist_ok=True)

    state_path = auth_dir / "niffler_user.json"

    context = browser.new_context()
    page = context.new_page()

    try:
        registration_page = AuthPage(page=page)
        registration_page.visit(envs.frontend_url)
        registration_page.login(username=envs.test_username, password=envs.test_password)
        registration_page.spending_title_exists("History of Spendings")

        # Сохраняем состояние аутентификации
        context.storage_state(path=state_path)

        print(f"Auth state saved to: {state_path}")

    except Exception as e:
        print(f"Error during authentication: {e}")
        raise
    finally:
        context.close()

    return state_path


@pytest.fixture(scope="function")
def chromium_page_with_state(browser: Browser, initialize_browser_state):
    """Страница с предустановленной авторизацией"""
    context = browser.new_context(storage_state=initialize_browser_state)
    page = context.new_page()

    yield page

    context.close()


@pytest.fixture(scope="function")
def spends_page(chromium_page_with_state: Page) -> SpendPage:
    spend_page = SpendPage(chromium_page_with_state)
    return spend_page


@pytest.fixture(scope="function")
def spends_page_late(chromium_page_with_state: Page, category, spends) -> SpendPage:
    spend_page = SpendPage(chromium_page_with_state)
    return spend_page


@pytest.fixture()
def open_spend_page(spends_page, envs):
    spends_page.visit(envs.frontend_url)
    spends_page.wait_for_load()
    spends_page.reload()


@pytest.fixture(scope="function")
def profile_page(chromium_page_with_state: Page) -> ProfilePage:
    profile_page = ProfilePage(chromium_page_with_state)
    return profile_page


@pytest.fixture()
def open_profile_page(profile_page, envs):
    profile_page.visit(envs.profile_url)
    profile_page.wait_for_load()


@pytest.fixture(scope="function")
def login_page(page: Page) -> AuthPage:
    login_page = AuthPage(page)
    return login_page


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



# @pytest.fixture(scope='function')
# def chromium_page(playwright) -> Page:
#     chromium = playwright.chromium.launch(headless=False)
#     yield chromium.new_page()


# @pytest.fixture
# def login_page(chromium_page: Page) -> AuthPage:
#     return AuthPage(page=chromium_page)


# @pytest.fixture(scope="function")
# def login_page(chromium_page: Page) -> AuthPage:
#     login_page = AuthPage(chromium_page)
#     return login_page


# @pytest.fixture(scope='function')
# def auth_pw_page(chromium_page: Page) -> AuthPage:
#     return AuthPage(chromium_page)


# @pytest.fixture
# def open_login_page(auth_pw_page, envs):
#     auth_pw_page.visit(envs.frontend_url)
#     auth_pw_page.wait_for_load()


# @pytest.fixture(scope="session")
# def app_user(envs):
#     """Данные пользователя из файла .env"""
#     return envs.test_username, envs.test_password
#
#
# @pytest.fixture(scope='session')
# def auth(envs) -> str:
#     """
#     Метод аутентификации пользователя посредством UI интерфейса
#     envs.frontend_url: url приложения http://frontend.niffler.dc
#     user: заранее созданный пользователь
#     :return: авторизационный id_token
#     """
#     browser.open(envs.frontend_url)
#     browser.element('input[name=username]').set_value(envs.test_username)
#     browser.element('input[name=password]').set_value(envs.test_password)
#     browser.element('button[type=submit]').click()
#     browser.element('[id="spendings"]').should(be.present)
#     return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


# @pytest.fixture()
# def delete_spend_fx(request, auth, envs):
#     name_category = request.param
#     yield name_category
#     spend_page.delete_spend(name_category)


#
# @pytest.fixture()
# def main_page(auth, envs):
#     """ Фикстура открывает главную страницу с аутентифицированным пользователем"""
#     browser.open(envs.frontend_url)


# @pytest.fixture()
# def main_page_late(category, spends, envs):
#     browser.open(envs.frontend_url)
#
#
# @pytest.fixture()
# def profile_page(auth, envs):
#     """Открытие страницы профиля аутентифицированного пользователя"""
#     browser.open(envs.profile_url)
#
#
# @pytest.fixture()
# def login_page(envs):
#     browser.open(envs.frontend_url)
#     yield
#     browser.quit()


# @pytest.fixture
# def auth_db(envs):
#     """ Метод авторизации для тестов с базой данных """
#     browser.open(envs.frontend_url)
#     browser.element('input[name=username]').set_value(envs.test_username)
#     browser.element('input[name=password]').set_value(envs.test_password)
#     browser.element('button[type=submit]').click()
#     yield
#     browser.quit()


# @pytest.fixture(scope='session')
# def category_client(envs, auth) -> CategoryHttpClient:
#     """
#     Метод возвращения instance класса CategoryHttpClient
#     :param envs: загрузка данный с env файла
#     :param auth: аутентификация пользователя
#     :return: instance  класса CategoryHttpClient
#     """
#     return CategoryHttpClient(envs.gateway_url, auth)


# @pytest.fixture(scope='session')
# def spends_client(envs, auth) -> SpendsHttpClient:
#     """
#     Метод возвращения instance класса SpendsHttpClient
#     :param envs: загрузка данный с env файла
#     :param auth: аутентификация пользователя
#     :return: instance класса SpendsHttpClient
#     """
#     return SpendsHttpClient(envs.gateway_url, auth)
