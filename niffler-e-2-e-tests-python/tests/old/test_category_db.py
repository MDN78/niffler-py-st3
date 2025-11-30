import pytest

from pages.spend_page import spend_page
from tools.helper import check_category_in_db, check_spend_in_db, delete_category_in_db

TEST_CATEGORY = "database"

@pytest.mark.skip
class TestDatabase:

    @pytest.mark.usefixtures("auth_db")
    def test_check_category_in_db(self, envs, spend_db):
        username = envs.test_username
        spend_page.create_spend(100, TEST_CATEGORY, "some")

        response = spend_db.get_user_categories(username)

        check_category_in_db(response, username, TEST_CATEGORY)

        spend_page.delete_spend_after_action()
        spend_db.delete_category(response[0].id)

    @pytest.mark.usefixtures("auth_db")
    def test_check_spend_in_db(self, envs, spend_db):
        username = envs.test_username
        spend_page.create_spend(100, TEST_CATEGORY, "some")

        response = spend_db.get_user_spends(username)
        check_spend_in_db(response, 100, TEST_CATEGORY, "some", username)

        spend_page.delete_spend_after_action()
        delete_category_in_db(response, spend_db)
