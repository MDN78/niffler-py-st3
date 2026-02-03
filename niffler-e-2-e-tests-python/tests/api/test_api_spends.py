import allure
import pytest
import time

from filelock import FileLock

from clients.spends_client import SpendsHttpClient
from marks import TestData
from models.category import CategoryAdd
from databases.spend_db import SpendDb
from models.spend import SpendAdd, Spend
from tools.assertions.base import assert_length
from tools.assertions.spends import assert_spend
from tools.allure.annotations import AllureFeature, AllureStory, AllureTags, AllureEpic

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]


@pytest.fixture(scope="module", autouse=True)
def module_fixture(tmp_path_factory, worker_id, spends_client: SpendsHttpClient, spend_db: SpendDb):
    """Подготовка модуля перед тестом - очистка базы"""
    def _prepare_state():
        categories_ids = spends_client.get_ids_all_categories()
        spend_db.delete_categories_by_ids(categories_ids)
        all_spends_ids = spends_client.get_ids_all_spending()
        for spend_id in all_spends_ids:
            spends_client.delete_spending_by_id(spend_id)

    if worker_id == "master":
        _prepare_state()

    root_tmp_dir = tmp_path_factory.getbasetemp().parent

    fn = root_tmp_dir / "prepare"
    with FileLock(str(fn) + ".lock"):
        if fn.is_file():
            pass
        else:
            _prepare_state()


@pytest.fixture(scope='function', autouse=True)
def wait_before_run_test():
    """Ожидание для отработки фикстуры модуля при параллельном запуске"""
    time.sleep(1)


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
    def test_add_spend_with_minimal_amount(self, spends_client: SpendsHttpClient, spend_db: SpendDb):
        request = SpendAdd(amount=0.01, category=CategoryAdd())
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
