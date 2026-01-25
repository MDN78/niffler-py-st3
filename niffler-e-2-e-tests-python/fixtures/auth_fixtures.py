import json
import allure
import pytest

from _pytest.fixtures import SubRequest
from allure_commons.types import AttachmentType
from playwright.sync_api import Browser
from app.pages.auth_page import AuthPage
from clients.auth_client import AuthClient
from models.config import Envs
from tools.helper import mock_static_resources


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


@pytest.fixture(scope="session")
def get_token_from_user_state(initialize_browser_state):
    """Метод получения аутентификационного токена с файла из временного хранилища"""
    with open(initialize_browser_state) as json_file:
        data = json.load(json_file)
        api_token = data['origins'][0]['localStorage'][3]['value']
    return api_token


@pytest.fixture(scope="session")
def auth_api_token(envs: Envs):
    """Метод получение аутентификационного токена через OAuth2"""
    token = AuthClient(envs).auth(envs.test_username, envs.test_password)
    allure.attach(token, name="token.txt", attachment_type=AttachmentType.TEXT)
    return token


@pytest.fixture(scope="session")
def auth_client(envs: Envs) -> AuthClient:
    """
    Метод возвращения instance класса AuthClient
    :param envs: загрузка данный с env файла
    :return: instance класса AuthClient
    """
    return AuthClient(envs)
