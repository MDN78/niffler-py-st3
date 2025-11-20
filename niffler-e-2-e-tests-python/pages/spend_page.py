from selene import browser, have, query


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
        """Метод удаления затраты по наименованию rfntujhbb
        :param name_category: yfbvtyjdfybt rfntujhbb
        """
        self.category_name(name_category).click()
        self.delete_button.click()
        self.delete_button_approve.click()

    def action_should_have_signal_text(self, text: str) -> None:
        """Метод проверки всплывающего сообщения об успешном действии
        :param text: текст сигнального сообщения"""
        self.description_successful_delete_spend.should(have.text(text))


spend_page = SpendPage()
