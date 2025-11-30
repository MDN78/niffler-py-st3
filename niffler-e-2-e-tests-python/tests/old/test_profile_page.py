from marks import Pages, TestData
from pages.profile_page import profiles_page
from tools.fakers import fake
import pytest

TEST_CATEGORY = "school"

@pytest.mark.skip
class TestCategoriesOld:

    @Pages.profile_page
    def test_create_category(self):
        new_category = fake.word()
        profiles_page.add_category(new_category)
        profiles_page.successful_adding(new_category)

    @Pages.profile_page
    def test_add_empty_name_category(self, profile_page):
        profiles_page.adding_empty_name_category()
        profiles_page.check_error_message("Error while adding category : Category can not be blank")

    @Pages.profile_page
    @TestData.category(TEST_CATEGORY)
    def test_add_same_category(self, category):
        same_category = category
        profiles_page.add_category(same_category)
        profiles_page.check_error_message(f"Error while adding category {same_category}: Cannot save duplicates")

@pytest.mark.skip
class TestProfileInfoOld:

    @Pages.profile_page
    def test_profile_title(self):
        profiles_page.check_profile_title('Profile')

    @Pages.profile_page
    def test_create_user_name(self):
        user_name = fake.user_name()
        profiles_page.add_user_name(user_name)
        profiles_page.check_successful_adding_name()
