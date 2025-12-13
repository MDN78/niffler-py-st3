import pytest
import allure
from marks import Pages, TestData
from models.category import CategoryAdd
from models.spend import SpendAdd
from tools.assertions.database import check_category_in_db, check_spend_in_db
from tools.allure.annotations import AllureFeature, AllureStory, AllureTags, AllureEpic

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]

TEST_CATEGORY = "database"


@allure.tag(AllureTags.ACTIONS_DB)
@allure.feature(AllureFeature.DATABASE)
class TestDatabase:

    @allure.story(AllureStory.CATEGORY)
    @Pages.open_spend_page
    @TestData.category(TEST_CATEGORY)
    @TestData.spends(SpendAdd(category=CategoryAdd(name=TEST_CATEGORY)))
    def test_check_category_in_database(self, category, spends, spends_page_late, spend_db, envs):
        username = envs.test_username
        response = spend_db.get_user_categories(username)

        check_category_in_db(response, username, TEST_CATEGORY)

    @allure.story(AllureStory.SPEND)
    @Pages.open_spend_page
    @TestData.category(TEST_CATEGORY)
    @TestData.spends(SpendAdd(amount=100, category=CategoryAdd(name=TEST_CATEGORY), description="some"))
    def test_check_spend_in_db(self, category, spends, spends_page_late, spend_db, envs):
        username = envs.test_username
        response = spend_db.get_user_spends(username)

        check_spend_in_db(response, 100, TEST_CATEGORY, "some", username)
