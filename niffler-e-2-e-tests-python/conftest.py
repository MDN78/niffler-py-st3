import os
import allure
import pytest

from pytest import Item, FixtureDef, FixtureRequest
from dotenv import load_dotenv

from databases.userdata_db import UserdataDb
from models.config import Envs
from tools.allure.reportet import allure_reporter, allure_logger
from tools.allure.environment import create_allure_environment_file

pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.pages_fixtures",
                  "fixtures.kafka_fixtures", "fixtures.soap_fixtures"]


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
        test_password=os.getenv("TEST_PASSWORD"),
        kafka_address=os.getenv("KAFKA_ADDRESS"),
        userdata_db_url=os.getenv("USERDATA_DB_URL"),
        auth_db_url=os.getenv("AUTH_DB_URL"),
        soap_address=os.getenv("SOAP_ADDRESS")
    )


# @pytest.fixture(scope="session")
# def db_client(envs: Envs) -> UserdataDb:
#     return UserdataDb(envs)


@pytest.fixture(scope="session", autouse=True)
def create_test_user(auth_client):
    """Создание тестового пользователя перед всеми тестами"""
    # existing_user = db_client.get_user(os.getenv("TEST_USERNAME"))
    # print(existing_user)
    # if not existing_user:
    auth_client.register(username=os.getenv("TEST_USERNAME"),password=os.getenv("TEST_PASSWORD"))
