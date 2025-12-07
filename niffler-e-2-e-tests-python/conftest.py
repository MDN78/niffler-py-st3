import os
import allure
import pytest

from pytest import Item, FixtureDef, FixtureRequest
from dotenv import load_dotenv
from models.config import Envs
from tools.allure.reportet import allure_reporter, allure_logger
from tools.allure.environment import create_allure_environment_file

pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.pages_fixtures"]


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
