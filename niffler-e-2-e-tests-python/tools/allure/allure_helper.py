import json
import allure
import curlify
from json import JSONDecodeError
from allure_commons.types import AttachmentType
from requests import Response
from tools.logger import get_logger

logger = get_logger("API REQUESTS")


def allure_attach_request(function):
    """Декоратор логироваания запроса, хедеров запроса, хедеров ответа в allure шаг и аллюр аттачмент и в консоль."""

    def wrapper(*args, **kwargs):
        method, endpoint = args[1], args[2]
        with allure.step(f"{method} {endpoint}"):

            response: Response = function(*args, **kwargs)

            curl = curlify.to_curl(response.request)
            url = response.request.url
            logger.info(f'API: Method and URL: {method} {url}')

            allure.attach(
                body=curl.encode("utf8"),
                name=f"Request {response.status_code}",
                attachment_type=AttachmentType.TEXT,
                extension=".txt"
            )
            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode("utf8"),
                    name=f"Response json {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                    extension=".json"
                )
            except JSONDecodeError:
                allure.attach(
                    body=response.text.encode("utf8"),
                    name=f"Response text {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                    extension=".txt")
            allure.attach(
                body=json.dumps(dict(response.headers, indent=4)).encode("utf8"),
                name=f"Response headers {response.status_code}",
                attachment_type=AttachmentType.JSON,
                extension=".json"
            )
        return response

    return wrapper
