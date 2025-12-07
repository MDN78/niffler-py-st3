import pytest
from tools.allure.annotations import AllureEpic

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]


def test_api(auth_api_token):
    print(auth_api_token)
