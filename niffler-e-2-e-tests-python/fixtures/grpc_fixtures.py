import pytest
import grpc
from grpc import insecure_channel
from models.config import Envs

from internal.grpc.interceptors.allure import AllureInterceptor
from internal.grpc.interceptors.logging import LoggingInterceptor
from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient


INTERCEPTORS = [
    LoggingInterceptor(),
    AllureInterceptor(),
]


@pytest.fixture(scope="session")
def grpc_client(envs: Envs) -> NifflerCurrencyServiceClient:
    """ Метод для подключения канала """
    channel = insecure_channel(envs.grpc_port)
    intercepted_channel = grpc.intercept_channel(channel, *INTERCEPTORS)
    return NifflerCurrencyServiceClient(intercepted_channel)
