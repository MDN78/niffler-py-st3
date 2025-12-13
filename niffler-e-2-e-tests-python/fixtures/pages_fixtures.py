import pytest

from playwright.sync_api import Page
from app.pages.auth_page import AuthPage
from app.pages.profile_page import ProfilePage
from app.pages.spend_page import SpendPage
from models.config import Envs


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
