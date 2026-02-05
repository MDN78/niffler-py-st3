import pytest
import allure

from clients.category_client import CategoryHttpClient
from databases.spend_db import SpendDb
from marks import TestData
from models.category import CategoryAdd
from tools.allure.annotations import AllureEpic, AllureTags, AllureFeature, AllureStory
from tools.assertions.base import assert_greater_than_zero
from tools.assertions.category import assert_category

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]


@allure.tag(AllureTags.ACTIONS_API)
@allure.feature(AllureFeature.CATEGORY)
class TestCategory:

    @allure.story(AllureStory.CATEGORY)
    def test_add_new_category(self, category_client: CategoryHttpClient, spend_db: SpendDb):
        category_name = (CategoryAdd()).name
        category = category_client.add_category((CategoryAdd(name=category_name)))

        assert_category(category, category_name)

        spend_db.delete_category(category.id)

    @allure.story(AllureStory.CATEGORY)
    @TestData.category("awesome")
    def test_get_all_categories(self, category, category_client: CategoryHttpClient, spend_db: SpendDb):
        categories = category_client.get_categories()

        assert_greater_than_zero(len(categories), category)
