from playwright.sync_api import Page
from app.pages.base_page import BasePage
from app.components.input import Input
from app.components.button import Button
from app.components.title import Title
from app.components.text import Text


class AuthPage(BasePage):
    """
    Класс взаимодействия с UI страницей логина и регистрации
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.username = Input(page, locator='input[name=username]', name='username')
        self.password = Input(page, locator='input[name=password]', name='password')
        self.submit_button = Button(page, locator='button[type=submit]', name='submit')
        self.spending_title = Text(page, locator='[id="spendings"]>h2', name='spending title')
        self.login_warning = Text(page, locator="[class='form__error-container'] p", name='login warning')
        self.unsuccessful_registration = Text(page, locator='.form__error', name='unsuccessful registration')
        self.register_form = Button(page, locator='[class="form__register"]', name='register button')
        self.submit_password_field = Input(page, locator='input[name=passwordSubmit]', name='submit password')
        self.successful_registration = Text(page, locator='.form__paragraph', name='successful registration')
        self.register_form_title = Title(page, locator='[id="register-form"]>h1', name='register form title')

    def login(self, username: str, password: str) -> None:
        """
        Метод аутентификации существующего пользователя
        :param username: Имя пользователя
        :param password: Пароль пользователя
        """

        self.username.fill(username)
        self.password.fill(password)
        self.submit_button.click()

    def open_registration_page(self) -> None:
        """
        Метод перехода на страницу регистрации
        """
        self.register_form.click()

    def register_form_should_have_title(self, title: str) -> None:
        """
        Метод проверки регистрационной формы на предмет наличия заголовка
        :param title: проверяемый заголовок
        """
        self.register_form_title.should_have_text(title)

    def registration_user(self, username: str, password: str) -> None:
        """
        Метод регистрации нового пользователя
        :param username: имя нового пользователя
        :param password: пароль нового пользователя
        """
        self.register_form.click()
        self.username.fill(username)
        self.password.fill(password)
        self.submit_password_field.fill(password)
        self.submit_button.click()

    def spending_title_exists(self, title: str) -> None:
        """
        Метод проверки заголовка страницы Затрат
        :param title: наименование заголовка
        """
        self.spending_title.should_have_text(title)

    def text_unsuccessful_login(self, text: str) -> None:
        """
        Метод проверки предупредительного оповещения о неудачной аутентификации
        :param text: проверяемый текст
        """
        text_from_ui = self.login_warning.get_locator().text_content()
        assert text in text_from_ui or "Bad credentials" in text_from_ui


    def text_unsuccessful_registration(self, text: str) -> None:
        """
        Метод проверки текста после неуспешной регистрации пользователя
        :param text: проверяемый текст
        """
        self.unsuccessful_registration.should_have_text(text)

    def text_should_be_visible(self, text: str) -> None:
        """
        Метод проверки текста после успешной регистрации пользователя
        :param text: проверяемый текст
        """
        self.successful_registration.should_have_text(text)
