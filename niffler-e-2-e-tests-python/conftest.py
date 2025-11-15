import os

import pytest
from dotenv import load_dotenv
from selene import browser

load_dotenv()


@pytest.fixture
def app_url():
    """Получение url приложения"""
    return os.getenv("APP_URL")


@pytest.fixture(scope='function', autouse=True)
def setup_browser(app_url):
    browser.config.base_url = app_url
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.open('/')
    yield
    browser.quit()
