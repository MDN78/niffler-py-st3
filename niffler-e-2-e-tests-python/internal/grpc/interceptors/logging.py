import grpc
from typing import Callable
from google.protobuf.message import Message

from tools.logger import get_logger

logger = get_logger("gRPC logging Interceptor")


class LoggingInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Метод добавления логирования в gRPC"""

    def intercept_unary_unary(self, continuation: Callable, client_call_details: grpc.ClientCallDetails,
                              request: Message) -> Callable:
        logger.info(f"Method {client_call_details.method}")
        logger.info(f"gRPC message {request.DESCRIPTOR.name}")
        logger.info(f"gRPC message {request}")
        response = continuation(client_call_details, request)
        return response
