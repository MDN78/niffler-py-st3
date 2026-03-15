import grpc
import pytest
import allure

from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from internal.pb.niffler_currency_pb2 import CalculateRequest, CurrencyValues
from tools.assertions.base import assert_equal
from tools.allure.annotations import AllureEpic, AllureTags, AllureFeature, AllureStory

pytestmark = [pytest.mark.allure_label(AllureEpic.NIFFLER, label_type="epic")]


@allure.tag(AllureTags.GRPC)
@allure.feature(AllureFeature.GRPC)
class TestCalculateRate:

    @allure.story(AllureStory.GRPC_CALCULATE_RATE)
    def test_calculate_rate(self, grpc_client: NifflerCurrencyServiceClient):
        response = grpc_client.calculate_rate(
            request=CalculateRequest(spendCurrency=CurrencyValues.EUR, desiredCurrency=CurrencyValues.RUB, amount=100)
        )
        assert_equal(response.calculatedAmount, 7200, "calculate rate EUR/RUB")

    @allure.story(AllureStory.GRPC_CALCULATE_RATE)
    def test_calculate_rate_without_desired_currency(self, grpc_client: NifflerCurrencyServiceClient):
        try:
            response = grpc_client.calculate_rate(
                request=CalculateRequest(spendCurrency=CurrencyValues.EUR, amount=100)
            )
        except grpc.RpcError as e:
            assert_equal(e.code(), grpc.StatusCode.UNKNOWN, "Status code")
            assert_equal(e.details(), "Application error processing RPC", "Checking error message")

    @allure.story(AllureStory.GRPC_CONVERSATION)
    @pytest.mark.parametrize("spend, spend_currency, desired_currency, expected_result", [
        (100.0, CurrencyValues.USD, CurrencyValues.RUB, 6666.67),
        (100.0, CurrencyValues.RUB, CurrencyValues.USD, 1.5),
        (100.0, CurrencyValues.USD, CurrencyValues.USD, 100.0),
    ])
    def test_currency_conversion(self,
                                 grpc_client: NifflerCurrencyServiceClient,
                                 spend: float, spend_currency: CurrencyValues,
                                 desired_currency: CurrencyValues, expected_result: float):
        response = grpc_client.calculate_rate(
            request=CalculateRequest(spendCurrency=spend_currency, desiredCurrency=desired_currency, amount=spend)
        )
        assert_equal(response.calculatedAmount, expected_result, "calculate currency conversation")
