import allure
import pytest
from google.protobuf import empty_pb2

from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from tools.assertions.base import assert_length

from tools.allure.annotations import AllureEpic, AllureTags, AllureFeature, AllureStory


pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]


@allure.tag(AllureTags.GRPC)
@allure.feature(AllureFeature.GRPC)
class TestGrpcCurrency:

    @allure.story(AllureStory.GRPC_GET_CURRENCIES)
    def test_get_all_currencies(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        # Передаем запрос с пустым телом
        response = grpc_client.get_all_currencies(empty_pb2.Empty())
        currencies_list= list(response.allCurrencies)
        expected_list = [None] * 4
        assert_length(currencies_list, expected_list, "Currencies list")
