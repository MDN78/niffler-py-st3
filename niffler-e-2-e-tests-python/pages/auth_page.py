from selene import browser, have


class AuthPage():
    """Класс взаимодействия с UI страницей логина и регистрации"""

    def __init__(self):
        self.spending_title = browser.element('[id="spendings"]')
        self.spending_bottom_title = browser.element('[class="MuiBox-root css-11i3wq6"]')
        self.register_form = browser.element('[class="form__register"]')
        self.username = browser.element('input[name=username]')
        self.password = browser.element('input[name=password]')
        self.submit_password_field = browser.element('input[name=passwordSubmit]')
        self.submit_button = browser.element('button[type=submit]')
        self.successful_registration = browser.element('.form__paragraph')
        self.unsuccessful_registration = browser.element('.form__error')
        self.register_form_title = browser.element('[id="register-form"]')

        self.login_warning = browser.element("form[action='/login'] p")

    def login(self, username: str, password: str) -> None:
        """
        Метод аутентификации существующего пользователя
        :param username: Имя пользователя
        :param password: Пароль пользователя
        """
        self.username.set_value(username)
        self.password.set_value(password)
        self.submit_button.click()

    def open_registration_page(self) -> None:
        """
        Метод перехода на страницу регистрации
        """
        self.register_form.click()

    def spending_title_exists(self, title: str) -> None:
        """
        Метод проверки заголовка страницы Затрат
        :param title: наименование заголовка
        """
        self.spending_title.should(have.text(title))

    def spending_bottom_title_exists(self, title: str) -> None:
        """
        Метод проверки наличия заголовка нижней части страницы трат
        :param title: Наименование заголовка
        """
        self.spending_bottom_title.should(have.text(title))

    def registration_user(self, username: str, password: str) -> None:
        """
        Метод регистрации нового пользователя
        :param username: имя нового пользователя
        :param password: пароль нового пользователя
        """
        self.register_form.click()
        self.username.set_value(username)
        self.password.set_value(password)
        self.submit_password_field.set_value(password)
        self.submit_button.click()

    def register_form_should_have_title(self, title: str) -> None:
        """
        Метод проверки регистрационной формы на предмет наличия заголовка
        :param title: проверяемый заголовок
        """
        self.register_form_title.should(have.text(title))

    def text_should_be_visible(self, text: str) -> None:
        """
        Метод проверки текста после успешной регистрации пользователя
        :param text: проверяемый текст
        """
        self.successful_registration.should(have.text(text))

    def text_unsuccessful_registration(self, text: str) -> None:
        """
        Метод проверки текста после неуспешной регистрации пользователя
        :param text: проверяемый текст
        """
        self.unsuccessful_registration.should(have.text(text))

    def text_unsuccessful_login(self, text: str) -> None:
        """
        Метод проверки предупредительного оповещения о неудачной аутентификации
        :param text: проверяемый текст
        """
        self.login_warning.should(have.text(text))


auth_page = AuthPage()
