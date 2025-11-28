from selene import browser, have, be
from selenium.webdriver.common.keys import Keys


class CategoryPage:
    """
    Класс взаимодействия с UI страницей Категории
    """

    def __init__(self):
        self.person_icon = browser.element('[data-testid="PersonIcon"]')
        self.profile = browser.element('//li[.="Profile"]')
        self.category_name = lambda name_category: browser.element(f'//span[.="{name_category}"]').should(
            have.text(f"{name_category}"))
        self.name = browser.element('input[name=category]')
        self.category_name = lambda name: browser.all('span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w').element_by(
            have.text(name))
        self.category_input = lambda name: browser.element(f'input[value="{name}"]')
        self.parent_element = browser.all('div:has(span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w)')
        self.archive_button = 'button[aria-label="Archive category"]'
        self.confirm_archive = browser.all('button[type=button]').element_by(have.text('Archive'))
        self.archived_button = browser.element('//span[.="Show archived"]')
        self.archived_category = lambda name: browser.all(
            'span.MuiChip-label.MuiChip-labelMedium.css-14vsv3w').element_by(
            have.text(name))

    def category_should_be_exist(self, name_category: str) -> None:
        self.person_icon.click()
        self.profile.click()
        self.category_name(name_category).click()

    @staticmethod
    def refresh_page() -> None:
        browser.driver.refresh()

    def edit_category_name(self, old_name: str, new_name: str) -> None:
        self.category_name(old_name).should(be.present).click()
        self.category_input(old_name).clear().should(be.blank).type(new_name)
        self.category_input(new_name).send_keys(Keys.ENTER)

    def archive_category(self, category_name: str) -> None:
        self.parent_element.element_by(have.text(category_name)).element(self.archive_button).click()
        # self.confirm_archive.click()
        self.confirm_archive.press_enter()

    def should_be_category_name(self, name: str) -> None:
        self.category_name(name).should(be.present)

    def check_archived_category(self, name: str) -> None:
        self.archived_button.click()
        self.archived_category(name)


category_page = CategoryPage()