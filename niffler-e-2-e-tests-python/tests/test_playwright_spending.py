from marks import Pages, TestData
from models.category import CategoryAdd
from models.spend import SpendAdd
from tools.fakers import fake
import pytest

TEST_CATEGORY = "school"
TEST_CATEGORY_1 = "car"
TEST_CATEGORY_2 = "city"
TEST_CATEGORY_3 = "country"


# @pytest.mark.skip
class TestSpendPage:

    # @pytest.mark.skip
    @Pages.open_spend_page
    def test_playwright_spending_title_statistic_exists(self, spends_page):
        spends_page.check_spending_page_titles('Statistics')

    # @pytest.mark.skip
    @Pages.open_spend_page
    def test_playwright_create_new_spending(self, spends_page):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()

        spends_page.create_spend(amount, category, description)
        spends_page.check_spending_exists(category)
        spends_page.delete_spend(category)

    # @pytest.mark.skip
    @Pages.open_spend_page
    def test_playwright_delete_spending_via_ui(self, spends_page):
        amount = fake.integer()
        category = fake.word()
        description = fake.user_name()

        spends_page.create_spend(amount, category, description)
        spends_page.delete_spend(category)
        spends_page.action_should_have_signal_text("Spendings succesfully deleted")

    # @pytest.mark.skip
    @Pages.open_spend_page
    @TestData.category(TEST_CATEGORY)
    @TestData.spends(SpendAdd(category=CategoryAdd(name=TEST_CATEGORY)))
    def test_delete_spending(self, category, spends, spends_page_late):
        # spends_page_late.reload()
        spends_page_late.delete_spend(TEST_CATEGORY)
        spends_page_late.action_should_have_signal_text("Spendings succesfully deleted")

    # @pytest.mark.skip
    @Pages.open_spend_page
    @TestData.category(TEST_CATEGORY_1)
    @TestData.spends(SpendAdd(description="QA.GURU Python Advanced 2", category=CategoryAdd(name=TEST_CATEGORY_1)))
    def test_delete_spending_after_action(self, category, spends, spends_page_late):
        # spends_page_late.reload()
        spends_page_late.spending_page_should_have_text("QA.GURU Python Advanced 2")
        spends_page_late.delete_spend_after_action()

    @Pages.open_spend_page
    @TestData.category(TEST_CATEGORY_2)
    @TestData.spends(SpendAdd(category=CategoryAdd(name=TEST_CATEGORY_2)))
    def test_delete_all_spending(self, category, spends, spends_page_late):
        # spends_page_late.reload()
        spends_page_late.check_delete_spending("Spendings succesfully deleted")


    @Pages.open_spend_page
    @TestData.category(TEST_CATEGORY_3)
    @TestData.spends(SpendAdd(category=CategoryAdd(name=TEST_CATEGORY_3)))
    def test_edit_spending_currency_usd(self, category, spends, spends_page_late):
        # spends_page_late.reload()
        spends_page_late.edit_spending_currency("USD")
        spends_page_late.should_be_signal_text("Spending is edited successfully")