from selene import browser, have, query, command


class SpendPage():
    """Класс взаимодействия с UI страницей spends"""

    def __init__(self):
        self.statistic_title = browser.element('[id="stat"] h2')
        self.new_spend_button = browser.element('//a[.="New spending"]')
        self.title_new_spending_list = browser.element('.MuiTypography-root.MuiTypography-h5.css-w1t7b3')
        self.amount = browser.element('#amount')
        self.category = browser.element('#category')
        self.description = browser.element('#description')
        self.button_add_spending = browser.element('#save')
        self.category_name = lambda name_category: browser.element('#spendings tbody').should(
            have.text(f"{name_category}"))
        self.delete_button = browser.element('#delete')
        self.delete_button_approve = browser.element("//div[@role='dialog']//button[contains(text(), 'Delete')]")
        self.spending = browser.element('#spendings')
        self.description_successful_delete_spend = browser.element('//div[.="Spendings succesfully deleted"]')
        self.spending_body = browser.element('#spendings tbody')

        self.checkbox_for_all = browser.element('thead input[type="checkbox"]')
        self.successful_delete = browser.element('.Toastify__toast-body div:nth-child(2)')

        self.edit_spending = browser.element('button[type=button][aria-label="Edit spending"]')
        self.currency = browser.element('#currency')
        self.select_currency = lambda currency: browser.element(f'//span[.="{currency}"]')
        self.button_save = browser.element('#save')
        self.successful_change = browser.element('//div[.="Spending is edited successfully"]')

        self.spending_tb = browser.element('#spendings tbody .MuiCheckbox-root')

    def check_spending_page_titles(self, text: str):
        """Метод проверки заголовка страницы затрат
        :param text: текст заголовка"""
        self.statistic_title.should(have.text(text))

    def create_spend(self, amount: int, test_category: str, description: str) -> None:
        """Метод создания траты
        :param amount: сумма затраты
        :param test_category: категория затрат
        :param description: описания затрат
        """
        self.new_spend_button.click()
        self.title_new_spending_list.should(have.text('Add new spending'))
        self.amount.set_value(amount)
        self.category.set_value(f'{test_category}')
        self.description.set_value(f'{description}')
        self.button_add_spending.click()

    def check_spending_exists(self, category: str, amount: str):
        """Метод проверки создания затраты
        :param category: наименование категории
        :param amount: сумма затрат
        """
        filtered_cells = browser.all('.table.spendings-table td').by(have.text(f'{category} {amount}'))
        for cell in filtered_cells:
            print(f"Найдена ячейка с текстом: {cell.get(query.text)}")

    def delete_spend(self, name_category: str) -> None:
        """Метод удаления затраты по наименованию категории
        :param name_category: наименование категории
        """
        self.category_name(name_category).click()
        self.delete_button.click()
        self.delete_button_approve.press_enter()

    def action_should_have_signal_text(self, text: str) -> None:
        """Метод проверки всплывающего сообщения об успешном действии
        :param text: текст сигнального сообщения"""
        self.description_successful_delete_spend.should(have.text(text))

    def spending_page_should_have_text(self, description: str):
        """
        Метод проверки описания на странице
        :param description: искомое описание
        """
        self.spending_body.perform(command.js.scroll_into_view)
        self.spending_body.should(have.text(description))

    def check_delete_spending(self, text: str):
        """
        Метод удаления и последующей проверки затрат
        :param text: текст итогового сообщения
        """
        # self.checkbox_for_all.click()
        self.checkbox_for_all.perform(command.js.scroll_into_view).click()
        self.delete_button.click()
        # self.delete_button_approve.click()
        self.delete_button_approve.press_enter()
        self.description_successful_delete_spend.should(have.text(text))

    def edit_spending_currency(self, currency: str):
        """
        Метод изменения валюты расходов
        :param currency: желаемая валюта в формате "USD"
        """
        self.edit_spending.click()
        self.currency.click()
        self.select_currency(currency).click()
        self.button_save.click()

    def should_be_signal_text(self, text: str) -> None:
        """Метод проверки всплывающего сообщения об успешном действии
        :param text: текст сигнального сообщения"""
        self.successful_change.should(have.text(text))


    def delete_spend_after_action(self):
        """
        Метод удаления всех трат после добавления через клиентов
        """
        self.checkbox_for_all.perform(command.js.scroll_into_view).click()
        # self.spending_tb.perform(command.js.scroll_into_view).click()
        self.delete_button.click()
        self.delete_button_approve.press_enter()
        self.spending.should(have.text("There are no spendings"))



spend_page = SpendPage()
