from tools.fakers import fake
from marks import TestData
from marks import Pages
import pytest
import allure
from tools.allure.annotations import AllureFeature, AllureStory

pytestmark = [pytest.mark.allure_label("Categories", label_type="epic")]

TEST_CATEGORY = "school"


# @pytest.mark.skip
@allure.tag(AllureFeature.CATEGORY)
class TestCategories:

    @allure.tag(AllureStory.CATEGORY)
    @Pages.open_profile_page
    def test_create_category(self, profile_page):
        new_category = fake.word()
        profile_page.add_category(new_category)
        profile_page.successful_adding(new_category)

    @allure.tag(AllureStory.CATEGORY)
    @Pages.open_profile_page
    def test_add_empty_name_category(self, profile_page):
        profile_page.adding_empty_name_category()
        profile_page.check_error_message("Error while adding category : Category can not be blank")

    @allure.tag(AllureStory.CATEGORY)
    @Pages.open_profile_page
    @TestData.category(TEST_CATEGORY)
    def test_add_same_category(self, category, profile_page):
        same_category = category
        profile_page.add_category(same_category)
        profile_page.check_error_message(f"Error while adding category {same_category}: Cannot save duplicates")


# @pytest.mark.skip
@allure.tag(AllureFeature.PROFILE)
class TestProfileInfo:

    @allure.tag(AllureStory.NAVIGATION)
    @Pages.open_profile_page
    def test_profile_title(self, profile_page):
        profile_page.check_profile_title('Profile')

    @allure.tag(AllureStory.NAVIGATION)
    @Pages.open_profile_page
    def test_create_user_name(self, profile_page):
        user_name = fake.user_name()
        profile_page.add_user_name(user_name)
        profile_page.check_successful_adding_name()
