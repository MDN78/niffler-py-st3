from playwright.sync_api import Page, expect
from app.pages.base_page import BasePage
from app.components.input import Input
from app.components.button import Button
from app.components.title import Title
from app.components.text import Text


class SpendPage(BasePage):
    """
    Класс взаимодействия с UI страницей spends
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.statistic_title = Title(page, locator='[id="stat"] h2', name='Statistics')
        self.new_spend_button = Button(page, locator='//a[.="New spending"]', name='New spend button')
        self.title_new_spending_list = Text(page, locator='.MuiTypography-root.MuiTypography-h5.css-w1t7b3',
                                            name='New spending title')
        self.amount = Input(page, locator='#amount', name='Amount')
        self.category = Input(page, locator='#category', name='Category')
        self.description = Input(page, locator='#description', name='Description')
        self.button_add_spending = Button(page, locator='#save', name='Add spending button')
        self.category_name = lambda name_category: (
            page.locator('#spendings tbody').locator(f":text('{name_category}')").first.click())
        self.delete_button = Button(page, locator='#delete', name='Button delete spend')
        self.delete_button_approve = Button(page,
                                            locator="//div[@role='dialog']//button[contains(text(), 'Delete')]",
                                            name='Confirm delete spend')

        self.description_successful_delete_spend = Text(page, locator="//div[@role='presentation']//div[contains(text(), 'Spendings succesfully deleted')]",
                                                        name='Description successful delete spend')
        self.spending_body = Text(page, locator='#spendings tbody >> text=QA.GURU Python Advanced 2', name='Spending body')
        #
        self.checkbox_for_all = Button(page, locator='thead input[type="checkbox"]', name='Checkbox for all')
        self.spending = Text(page, locator='[id="spendings"]>div', name='Spendings')
        # self.successful_delete = browser.element('.Toastify__toast-body div:nth-child(2)')
        #
        # self.edit_spending = browser.element('button[type=button][aria-label="Edit spending"]')
        # self.currency = browser.element('#currency')
        # self.select_currency = lambda currency: browser.element(f'//span[.="{currency}"]')
        # self.button_save = browser.element('#save')
        # self.successful_change = browser.element('//div[.="Spending is edited successfully"]')
        #
        # self.spending_tb = browser.element('#spendings tbody .MuiCheckbox-root')

    def check_spending_page_titles(self, text: str):
        """Метод проверки заголовка страницы затрат
        :param text: текст заголовка"""
        self.statistic_title.should_have_text(text)

    def create_spend(self, amount: int, test_category: str, description: str) -> None:
        """Метод создания траты
        :param amount: сумма затраты
        :param test_category: категория затрат
        :param description: описания затрат
        """
        self.new_spend_button.click()
        self.title_new_spending_list.should_have_text('Add new spending')
        self.amount.fill(str(amount))
        self.category.fill(f'{test_category}')
        self.description.fill(f'{description}')
        self.button_add_spending.click()

    def check_spending_exists(self, category: str):
        """Метод проверки создания затраты
        :param category: наименование категории
        """
        filtered_cells = self.page.locator('.table.spendings-table td').filter(has_text=category).all()

    def delete_spend(self, name_category: str) -> None:
        """Метод удаления затраты по наименованию категории
        :param name_category: наименование категории
        """
        self.category_name(name_category)
        self.delete_button.click()
        self.delete_button_approve.click()

    def action_should_have_signal_text(self, text: str) -> None:
        """Метод проверки всплывающего сообщения об успешном действии
        :param text: текст сигнального сообщения"""
        self.description_successful_delete_spend.should_have_text(text)


    def spending_page_should_have_text(self, description: str):
        """
        Метод проверки описания на странице
        :param description: искомое описание
        """
        self.spending_body.should_have_text(description)
        # self.spending_body.perform(command.js.scroll_into_view)
        # self.spending_body.should(have.text(description))
    #
    # def check_delete_spending(self, text: str):
    #     """
    #     Метод удаления и последующей проверки затрат
    #     :param text: текст итогового сообщения
    #     """
    #     # self.checkbox_for_all.click()
    #     self.checkbox_for_all.perform(command.js.scroll_into_view).click()
    #     self.delete_button.click()
    #     # self.delete_button_approve.click()
    #     self.delete_button_approve.press_enter()
    #     self.description_successful_delete_spend.should(have.text(text))
    #
    # def edit_spending_currency(self, currency: str):
    #     """
    #     Метод изменения валюты расходов
    #     :param currency: желаемая валюта в формате "USD"
    #     """
    #     self.edit_spending.click()
    #     self.currency.click()
    #     self.select_currency(currency).click()
    #     self.button_save.click()
    #
    # def should_be_signal_text(self, text: str) -> None:
    #     """Метод проверки всплывающего сообщения об успешном действии
    #     :param text: текст сигнального сообщения"""
    #     self.successful_change.should(have.text(text))
    #
    #
    def delete_spend_after_action(self):
        """
        Метод удаления всех трат после добавления через клиентов
        """
        self.checkbox_for_all.click()
        # self.checkbox_for_all.perform(command.js.scroll_into_view).click()
        # self.spending_tb.perform(command.js.scroll_into_view).click()
        self.delete_button.click()
        self.delete_button_approve.click()
        self.description_successful_delete_spend.should_have_text("Spendings succesfully deleted")
