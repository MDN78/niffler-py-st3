import allure
import pytest
from http import HTTPStatus

from resources.templates.read_templates import current_user_xml
from tools.soap.xml_operation import current_user_result_operation
from tools.assertions.base import assert_status_code
from tools.assertions.soap import assert_userdata, assert_unknown_userdata
from tools.fakers import fake
from tools.allure.annotations import AllureEpic, AllureTags, AllureFeature, AllureStory

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]


@allure.tag(AllureTags.SOAP)
@allure.feature(AllureFeature.SOAP)
class TestSoapNiffler:

    @allure.story(AllureStory.SOAP_GET_USER_INFO)
    def test_get_user_info_by_exist_username(self, soap_session, envs):
        response = soap_session.request(data=current_user_xml(envs.test_username))
        user_data = current_user_result_operation(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_userdata(user_data, envs.test_username)

    @allure.story(AllureStory.SOAP_GET_USER_INFO)
    def test_get_user_info_by_not_exist_username(self, soap_session):
        user_name = fake.user_name()
        response = soap_session.request(data=current_user_xml(user_name))
        user_data = current_user_result_operation(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_unknown_userdata(user_data, user_name)
