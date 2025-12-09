import allure
import pytest
from clients.spends_client import SpendsHttpClient
from marks import TestData
from models.category import CategoryAdd
from databases.spend_db import SpendDb
from models.spend import SpendAdd, Spend
from tools.assertions.base import assert_length
from tools.assertions.spends import assert_spend
from tools.allure.annotations import AllureFeature, AllureStory, AllureTags, AllureEpic

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]


@allure.tag(AllureTags.ACTIONS_API)
@allure.feature(AllureFeature.SPENDS)
class TestApiSpends:

    @allure.story(AllureStory.AUTHENTICATION)
    def test_api_auth(self, auth_api_token):
        assert auth_api_token is not None

    @allure.story(AllureStory.SPEND)
    def test_add_spend(self, spends_client: SpendsHttpClient, spend_db: SpendDb):
        request = SpendAdd(category=CategoryAdd())
        response = spends_client.add_spends(request)

        assert_spend(response, request)

        spends_client.remove_spends([response.id])
        spend_db.delete_category(response.category.id)

    @allure.story(AllureStory.SPEND)
    def test_add_spend_with_category_name(self, spends_client: SpendsHttpClient, spend_db: SpendDb):
        request = SpendAdd(category=CategoryAdd(name="QA.GURU"), description="New description")
        response = spends_client.add_spends(request)

        assert_spend(response, request)

        spends_client.remove_spends([response.id])
        spend_db.delete_category(response.category.id)

    @allure.story(AllureStory.SPEND)
    def test_add_spend_without_description(self, spends_client: SpendsHttpClient, spend_db: SpendDb):
        request = SpendAdd(category=CategoryAdd(), description="")
        response = spends_client.add_spends(request)

        assert_spend(response, request)

        spends_client.remove_spends([response.id])
        spend_db.delete_category(response.category.id)

    @allure.story(AllureStory.SPEND)
    @TestData.spends(SpendAdd(category=CategoryAdd()))
    def test_remove_spend(self, spends, spend_db: SpendDb, spends_client: SpendsHttpClient):
        spends_client.remove_spends([spends.id])
        response = spends_client.get_spends()
        assert_length(response, [], 'Model spends')
        spend_db.delete_category(spends.category.id)

    @allure.story(AllureStory.SPEND)
    @TestData.category('vehicles')
    @TestData.spends(SpendAdd(category=CategoryAdd(name='vehicles')))
    def test_update_spend_description(self, category, spends, spends_client: SpendsHttpClient, spend_db):
        updated_info = Spend(
            id=spends.id,
            spendDate=spends.spendDate,
            category=spends.category,
            currency=spends.currency,
            amount=spends.amount,
            description='for test',
            username=spends.username
        )
        updated_spend = spends_client.update_spend(updated_info)
        assert_spend(updated_spend, updated_info)

    @allure.story(AllureStory.SPEND)
    @TestData.category('vehicles')
    @TestData.spends(SpendAdd(category=CategoryAdd(name='vehicles')))
    def test_update_spend_currency_eur(self, category, spends, spends_client: SpendsHttpClient, spend_db):
        updated_info = Spend(
            id=spends.id,
            spendDate=spends.spendDate,
            category=spends.category,
            currency="EUR",
            amount=spends.amount,
            description=spends.description,
            username=spends.username
        )
        updated_spend = spends_client.update_spend(updated_info)
        assert_spend(updated_spend, updated_info)
