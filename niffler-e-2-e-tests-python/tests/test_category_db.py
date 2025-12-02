from marks import Pages, TestData
from models.category import CategoryAdd
from models.spend import SpendAdd
import pytest
from tools.helper import check_category_in_db, check_spend_in_db
import allure
from tools.allure.annotations import AllureFeature, AllureStory

pytestmark = [pytest.mark.allure_label("Database", label_type="epic")]

TEST_CATEGORY = "database"


# @pytest.mark.skip
@allure.tag(AllureFeature.DATABASE)
class TestDatabase:


    @Pages.open_spend_page
    @TestData.category(TEST_CATEGORY)
    @TestData.spends(SpendAdd(category=CategoryAdd(name=TEST_CATEGORY)))
    @allure.tag(AllureStory.CATEGORY)
    def test_check_category_in_database(self, category, spends, spends_page_late, spend_db, envs):
        spends_page_late.reload()
        username = envs.test_username
        response = spend_db.get_user_categories(username)

        check_category_in_db(response, username, TEST_CATEGORY)


    @Pages.open_spend_page
    @TestData.category(TEST_CATEGORY)
    @TestData.spends(SpendAdd(amount=100, category=CategoryAdd(name=TEST_CATEGORY), description="some"))
    @allure.tag(AllureStory.SPEND)
    def test_check_spend_in_db(self, category, spends, spends_page_late, spend_db, envs):
        spends_page_late.reload()
        username = envs.test_username

        response = spend_db.get_user_spends(username)
        check_spend_in_db(response, 100, TEST_CATEGORY, "some", username)
