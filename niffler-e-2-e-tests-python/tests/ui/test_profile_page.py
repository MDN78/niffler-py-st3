from tools.fakers import fake
from marks import TestData
from marks import Pages
import pytest
import allure
from tools.allure.annotations import AllureFeature, AllureStory, AllureTags, AllureEpic

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]

TEST_CATEGORY = "school"


# @pytest.mark.skip
@allure.tag(AllureTags.ACTIONS_UI)
@allure.feature(AllureFeature.CATEGORY)
class TestCategories:

    @allure.story(AllureStory.CATEGORY)
    @Pages.open_profile_page
    def test_create_category(self, profile_page):
        new_category = fake.word()
        profile_page.add_category(new_category)
        profile_page.successful_adding(new_category)

    @allure.story(AllureStory.CATEGORY)
    @Pages.open_profile_page
    def test_add_empty_name_category(self, profile_page):
        profile_page.adding_empty_name_category()
        profile_page.check_error_message("Error while adding category : Category can not be blank")

    @allure.story(AllureStory.CATEGORY)
    @Pages.open_profile_page
    @TestData.category(TEST_CATEGORY)
    def test_add_same_category(self, category, profile_page):
        same_category = category
        profile_page.add_category(same_category)
        profile_page.check_error_message(f"Error while adding category {same_category}: Cannot save duplicates")


# @pytest.mark.skip
@allure.tag(AllureTags.ACTIONS_UI)
@allure.feature(AllureFeature.PROFILE)
class TestProfileInfo:

    @allure.story(AllureStory.NAVIGATION)
    @Pages.open_profile_page
    def test_profile_title(self, profile_page):
        profile_page.check_profile_title('Profile')

    @allure.story(AllureStory.NAVIGATION)
    @Pages.open_profile_page
    def test_create_user_name(self, profile_page):
        user_name = fake.user_name()
        profile_page.add_user_name(user_name)
        profile_page.check_successful_adding_name()
