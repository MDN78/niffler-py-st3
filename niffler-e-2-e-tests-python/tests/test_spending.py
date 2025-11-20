from marks import Pages, TestData
from pages.spend_page import spend_page
from tools.fakers import fake

TEST_CATEGORY = "school"


class TestSpendPage:

    @Pages.main_page
    def test_spending_title_statistic_exists(self):
        spend_page.check_spending_page_titles('Statistics')

    def test_create_new_spending(self, auth, delete_spends):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()

        spend_page.create_spend(amount, category, description)
        spend_page.check_spending_exists(category, amount)

    def test_delete_spending(self, auth):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()

        spend_page.create_spend(amount, category, description)
        spend_page.delete_spend(category)
        spend_page.action_should_have_signal_text("Spendings succesfully delete")

    @Pages.main_page_late
    @TestData.category(TEST_CATEGORY)
    @TestData.spends({
        "amount": "108.51",
        "description": "QA.GURU Python Advanced 1",
        "category": {
            "name": TEST_CATEGORY
        },
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    })
    def test_delete_spending_after_table_action(self, category, spends):
        spend_page.spending_page_should_have_text("QA.GURU Python Advanced 1")

    @Pages.main_page_late
    @TestData.category(TEST_CATEGORY)
    @TestData.spends({
        "amount": "108.51",
        "description": "QA.GURU Python Advanced 1",
        "category": {
            "name": TEST_CATEGORY
        },
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    })
    def test_delete_all_spending(self, category, spends):
        spend_page.check_delete_spending("Spendings succesfully deleted")

    @Pages.main_page_late
    @TestData.category(TEST_CATEGORY)
    @TestData.spends({
        "amount": "108.51",
        "description": "QA.GURU Python Advanced 1",
        "category": {
            "name": TEST_CATEGORY
        },
        "spendDate": "2024-08-08T18:39:27.955Z",
        "currency": "RUB"
    })
    def test_edit_spending_currency_usd(self, category, spends):
        spend_page.edit_spending_currency("USD")
        spend_page.should_be_signal_text("Spending is edited successfully")
