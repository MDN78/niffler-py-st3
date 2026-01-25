import pytest
import allure

from tools.fakers import fake
from marks import Pages
from tools.allure.annotations import AllureFeature, AllureStory, AllureTags, AllureEpic

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]


@allure.tag(AllureTags.ACTIONS_UI)
@allure.feature(AllureFeature.AUTHENTICATION)
class TestAuthentication:

    @allure.story(AllureStory.REGISTRATION)
    @Pages.open_login_page
    def test_registration_new_user(self, login_page, envs):
        login_page.registration_user(fake.user_name(), fake.password())
        login_page.text_should_be_visible("Congratulations! You've registered!")

    @allure.story(AllureStory.AUTHENTICATION)
    @Pages.open_login_page
    def test_authentication_user(self, login_page, envs):
        login_page.login(envs.test_username, envs.test_password)
        login_page.spending_title_exists("History of Spendings")

    @allure.story(AllureStory.NAVIGATION)
    @Pages.open_login_page
    def test_navigate_from_authorization_to_registration(self, login_page, envs):
        login_page.open_registration_page()
        login_page.register_form_should_have_title('Sign up')

    @allure.story(AllureStory.WRONG_AUTHENTICATION)
    @Pages.open_login_page
    def test_login_user_with_invalid_login_or_password(self, login_page, envs):
        login_page.login('username', 'password')
        login_page.text_unsuccessful_login("Неверные учетные данные пользователя")

    @allure.story(AllureStory.WRONG_AUTHENTICATION)
    @Pages.open_login_page
    def test_registration_new_user_with_forbidden_name(self, login_page, envs):
        login_page.registration_user('ws', envs.test_password)
        login_page.text_unsuccessful_registration("Allowed username length should be from 3 to 50 characters")
