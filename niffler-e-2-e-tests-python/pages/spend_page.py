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

    def check_spending_page_titles(self, text: str):
        self.statistic_title.should(have.text(text))

    def create_spend(self, amount: int, test_category: str, description: str) -> None:
        self.new_spend_button.click()
        self.title_new_spending_list.should(have.text('Add new spending'))
        self.amount.set_value(amount)
        self.category.set_value(f'{test_category}')
        self.description.set_value(f'{description}')
        self.button_add_spending.click()

    def check_spending_exists(self, category: str, amount: str):
        filtered_cells = browser.all('.table.spendings-table td').by(have.text(f'{category} {amount}'))
        for cell in filtered_cells:
            print(f"Найдена ячейка с текстом: {cell.get(query.text)}")

spend_page = SpendPage()
