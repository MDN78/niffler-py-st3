import os

from pages.auth_page import auth_page
from tools.fakers import fake


class TestAuthentication:

    def test_registration_new_user(self):
        auth_page.open_auth_page()
        auth_page.registration_user(fake.user_name(), fake.password())
        auth_page.text_should_be_visible("Congratulations! You've registered!")

    def test_login_user(self):
        auth_page.open_auth_page()
        auth_page.login(os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD"))
        auth_page.spending_title_exists("History of Spendings")

    def test_navigate_from_authorization_to_registration(self):
        auth_page.open_auth_page()
        auth_page.open_registration_page()
        auth_page.register_form_should_have_title('Sign up')

    def test_login_user_with_invalid_login_or_password(self):
        auth_page.open_auth_page()
        auth_page.login("username", "password")
        auth_page.text_unsuccessful_login('Неверные учетные данные пользователя')

    def test_registration_new_user_with_forbidden_name(self):
        auth_page.open_auth_page()
        auth_page.registration_user('ws', fake.password())
        auth_page.text_unsuccessful_registration("Allowed username length should be from 3 to 50 characters")
