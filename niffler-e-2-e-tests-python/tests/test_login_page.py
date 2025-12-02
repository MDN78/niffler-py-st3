from tools.fakers import fake
from marks import Pages
import pytest


# @pytest.mark.skip
class TestAuthentication:

    @Pages.open_login_page
    def test_registration_new_user(self, login_page, envs):
        login_page.registration_user(fake.user_name(), fake.password())
        login_page.text_should_be_visible("Congratulations! You've registered!")

    @Pages.open_login_page
    def test_authentication_user(self, login_page, envs):
        login_page.login(envs.test_username, envs.test_password)
        login_page.spending_title_exists("History of Spendings")

    @Pages.open_login_page
    def test_navigate_from_authorization_to_registration(self, login_page, envs):
        login_page.open_registration_page()
        login_page.register_form_should_have_title('Sign up')

    @Pages.open_login_page
    def test_login_user_with_invalid_login_or_password(self, login_page, envs):
        login_page.login('username', 'password')
        login_page.text_unsuccessful_login("Неверные учетные данные пользователя")

    @Pages.open_login_page
    def test_registration_new_user_with_forbidden_name(self, login_page, envs):
        login_page.registration_user('ws', envs.test_password)
        login_page.text_unsuccessful_registration("Allowed username length should be from 3 to 50 characters")
