from tools.fakers import fake
from marks import TestData
from marks import Pages
import pytest

from tools.helper import delete_category_in_db

TEST_CATEGORY = "school"


# @pytest.mark.skip
class TestCategories:

    @Pages.open_profile_page
    def test_create_category(self, profile_page):
        new_category = fake.word()
        profile_page.add_category(new_category)
        profile_page.successful_adding(new_category)

    @Pages.open_profile_page
    def test_add_empty_name_category(self, profile_page):
        profile_page.adding_empty_name_category()
        profile_page.check_error_message("Error while adding category : Category can not be blank")

    @Pages.open_profile_page
    @TestData.category(TEST_CATEGORY)
    def test_add_same_category(self, category, profile_page):
        same_category = category
        profile_page.add_category(same_category)
        profile_page.check_error_message(f"Error while adding category {same_category}: Cannot save duplicates")


# @pytest.mark.skip
class TestProfileInfo:

    @Pages.open_profile_page
    def test_profile_title(self, profile_page):
        profile_page.check_profile_title('Profile')

    @Pages.open_profile_page
    def test_create_user_name(self, profile_page):
        user_name = fake.user_name()
        profile_page.add_user_name(user_name)
        profile_page.check_successful_adding_name()
