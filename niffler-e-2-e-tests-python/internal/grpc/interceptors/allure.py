import allure
import grpc
from typing import Callable
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToJson

from tools.logger import get_logger

logger = get_logger("gRPC Allure logging Interceptor")


class AllureInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Метод добавления логирования gRPC в allure"""

    def intercept_unary_unary(self, continuation: Callable, client_call_details: grpc.ClientCallDetails,
                              request: Message) -> Callable:
        with allure.step(client_call_details.method):
            logger.info(f"gRPC Allure Method {client_call_details.method}")
            allure.attach(MessageToJson(request), "request", attachment_type=allure.attachment_type.JSON)
            response = continuation(client_call_details, request)
            allure.attach(MessageToJson(response.result()), "response", attachment_type=allure.attachment_type.JSON)
        return response
