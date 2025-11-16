
from pages.spend_page import spend_page
from tools.fakers import fake


class TestSpendPage:

    def test_spending_title_statistic_exists(self, auth_ui):
        spend_page.check_spending_page_titles('Statistics')


    def test_create_new_spending(self, auth_ui):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()

        spend_page.create_spend(amount, category, description)
        spend_page.check_spending_exists(category, amount)