from playwright.sync_api import Page
from app.pages.base_page import BasePage
from app.components.input import Input
from app.components.button import Button
from app.components.title import Title
from app.components.text import Text


class ProfilePage(BasePage):
    """
    Класс взаимодействия с UI страницей Профиля пользователя
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.input_category = Input(page, locator='#category', name='input category')
        self.alert = Text(page, locator='div[role="alert"] div:nth-child(2)', name='alert')
        self.error_alert = Text(page, locator='.add-category__input-container button', name='error alert')
        self.name = Input(page, locator='#name', name='name')
        self.submit_button = Button(page, locator='button[type=submit]', name='submit')
        self.profile_title = Title(page, locator='.MuiTypography-root.MuiTypography-h5.css-w1t7b3', name='title')

    def add_category(self, category):
        """
        Метод добавления категории
        :param category: наименование категории
        """
        self.input_category.fill(category)
        self.page.keyboard.press('Enter')

    def successful_adding(self, category: str):
        """
        Метод проверки сигнального сообщения об успешном добавлении категории
        :param category: наименование категории
        """
        self.alert.should_have_text(f"You've added new category: {category}")

    def adding_empty_name_category(self):
        """
        Метод добавления категории без наименования
        """
        self.input_category.fill('  ')
        self.page.keyboard.press('Enter')

    def check_error_message(self, message: str):
        """
        Метод проверки alert сообщения
        """
        self.alert.should_have_text(message)

    def add_user_name(self, name: str):
        """
        Метод добавления имени в профиле пользователя
        :param name: имя пользователя
        """
        self.name.clear()
        self.name.fill(name)
        self.submit_button.click()

    def check_successful_adding_name(self):
        """
        Метод проверки сигнального сообщения об успешном добавлении имени пользователя
        """
        self.alert.should_have_text("Profile successfully updated")

    #
    def check_profile_title(self, title: str):
        """
        Метод проверки заголовка профайла пользователя
        :param title: Заголовок профайла
        """
        self.profile_title.should_have_text(title)
