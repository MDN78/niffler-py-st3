from tools.fakers import fake
from marks import Pages
import pytest
import allure
from tools.allure.annotations import AllureFeature, AllureStory

pytestmark = [pytest.mark.allure_label("Authentication", label_type="epic")]


# @pytest.mark.skip
@allure.tag(AllureFeature.AUTHENTICATION)
class TestAuthentication:

    @Pages.open_login_page
    @allure.tag(AllureStory.REGISTRATION)
    def test_registration_new_user(self, login_page, envs):
        login_page.registration_user(fake.user_name(), fake.password())
        login_page.text_should_be_visible("Congratulations! You've registered!")

    @Pages.open_login_page
    @allure.tag(AllureStory.AUTHENTICATION)
    def test_authentication_user(self, login_page, envs):
        login_page.login(envs.test_username, envs.test_password)
        login_page.spending_title_exists("History of Spendings")

    @Pages.open_login_page
    @allure.tag(AllureStory.NAVIGATION)
    def test_navigate_from_authorization_to_registration(self, login_page, envs):
        login_page.open_registration_page()
        login_page.register_form_should_have_title('Sign up')

    @Pages.open_login_page
    @allure.tag(AllureStory.WRONG_AUTHENTICATION)
    def test_login_user_with_invalid_login_or_password(self, login_page, envs):
        login_page.login('username', 'password')
        login_page.text_unsuccessful_login("Неверные учетные данные пользователя")

    @Pages.open_login_page
    @allure.tag(AllureStory.WRONG_AUTHENTICATION)
    def test_registration_new_user_with_forbidden_name(self, login_page, envs):
        login_page.registration_user('ws', envs.test_password)
        login_page.text_unsuccessful_registration("Allowed username length should be from 3 to 50 characters")
