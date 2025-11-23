from marks import TestData, Pages
from models.category import CategoryAdd
from models.spend import SpendAdd
import pytest


# тест крашит все остальные


TEST_CATEGORY = "school123456"


@pytest.mark.skip
@Pages.main_page_late
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendAdd(category=CategoryAdd(name=TEST_CATEGORY)))
def test_check_category_in_db(category, spends, spend_db, envs):
    username = envs.test_username
    spend_from_db = spend_db.get_user_categories(username)
    print(spend_from_db)

    first_category = spend_from_db[0]
    assert first_category.username == username
    assert first_category.name == TEST_CATEGORY

