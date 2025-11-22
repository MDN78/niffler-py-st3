from marks import Pages, TestData
from models.category import CategoryAdd
from models.spend import SpendAdd
from pages.spend_page import spend_page
from tools.fakers import fake

TEST_CATEGORY = "school"
TEST_CATEGORY_1 = "car"
TEST_CATEGORY_2 = "city"
TEST_CATEGORY_3 = "country"


class TestSpendPage:

    @Pages.main_page
    def test_spending_title_statistic_exists(self):
        spend_page.check_spending_page_titles('Statistics')

    def test_create_new_spending(self, auth):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()

        spend_page.create_spend(amount, category, description)
        spend_page.check_spending_exists(category, amount)
        spend_page.delete_spend(category)

    def test_delete_spending_via_ui(self, auth):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()

        spend_page.create_spend(amount, category, description)
        spend_page.delete_spend(category)
        spend_page.action_should_have_signal_text("Spendings succesfully delete")

    @Pages.main_page_late
    @TestData.category(TEST_CATEGORY)
    @TestData.spends(SpendAdd(
        amount=108.51,
        description="QA.GURU Python Advanced 1",
        category=CategoryAdd(name=TEST_CATEGORY),
        spendDate="2024-08-08T18:39:27.955Z",
        currency="RUB",
    ))
    def test_delete_spending(self, category, spends):
        spend_page.delete_spend(TEST_CATEGORY)
        spend_page.action_should_have_signal_text("Spendings succesfully delete")

    @Pages.main_page_late
    @TestData.category(TEST_CATEGORY_1)
    @TestData.spends(SpendAdd(
        amount=108.51,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=TEST_CATEGORY_1),
        spendDate="2024-08-08T18:39:27.955Z",
        currency="RUB",
    ))
    def test_delete_spending_after_action(self, category, spends):
        spend_page.spending_page_should_have_text("QA.GURU Python Advanced 2")
        spend_page.delete_spend_after_action()

    @Pages.main_page_late
    @TestData.category(TEST_CATEGORY_2)
    @TestData.spends(SpendAdd(
        amount=108.51,
        description="QA.GURU Python Advanced 3",
        category=CategoryAdd(name=TEST_CATEGORY_2),
        spendDate="2024-08-08T18:39:27.955Z",
        currency="RUB",
    ))
    def test_delete_all_spending(self, category, spends):
        spend_page.check_delete_spending("Spendings succesfully deleted")

    @Pages.main_page_late
    @TestData.category(TEST_CATEGORY_3)
    @TestData.spends(SpendAdd(
        amount=108.51,
        description="QA.GURU Python Advanced 4",
        category=CategoryAdd(name=TEST_CATEGORY_3),
        spendDate="2024-08-08T18:39:27.955Z",
        currency="RUB",
    ))
    def test_edit_spending_currency_usd(self, category, spends):
        spend_page.edit_spending_currency("USD")
        spend_page.should_be_signal_text("Spending is edited successfully")
