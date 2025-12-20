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
        from jinja2 import Environment, PackageLoader, select_autoescape
        new_env = Environment(loader=PackageLoader("resources"), autoescape=select_autoescape())

        # Загружаем оба шаблона
        request_template = new_env.get_template('colored_request.ftl')
        response_template = new_env.get_template('colored_response.ftl')

        with allure.step(f"{method} {endpoint}"):
            response: Response = function(*args, **kwargs)
            curl = curlify.to_curl(response.request)

            # Подготовка данных для шаблона request
            prepare_request_render = {
                "request": response.request,
                "curl": curl,
            }
            request_render = request_template.render(prepare_request_render)

            # Подготовка данных для шаблона response
            try:
                response_json = json.dumps(response.json(), indent=4, ensure_ascii=False)
                response_text = None
            except (JSONDecodeError, TypeError):
                response_json = None
                response_text = response.text

            # Получаем cookies из response
            response_cookies = {}
            if hasattr(response, 'cookies'):
                # Преобразуем RequestsCookieJar в обычный dict
                response_cookies = {cookie.name: cookie.value for cookie in response.cookies}

            prepare_response_render = {
                "response": response,
                "response_json": response_json,
                "response_text": response_text,
                "response_cookies": response_cookies,
            }
            response_render = response_template.render(prepare_response_render)

            url = response.request.url
            logger.info(f'API: Method and URL: {method} {url}')

            # Attach request template
            allure.attach(
                body=request_render.encode('utf-8'),
                name=f"Request",
                attachment_type=AttachmentType.HTML,
                extension=".html"
            )
            # Attach response template
            allure.attach(
                body=response_render.encode('utf-8'),
                name=f"Response {response.status_code}",
                attachment_type=AttachmentType.HTML,
                extension=".html"
            )
            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode("utf8"),
                    name=f"Response json {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                    extension=".json"
                )
            except (JSONDecodeError, TypeError):
                allure.attach(
                    body=response.text.encode("utf8"),
                    name=f"Response text {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                    extension=".txt"
                )
        return response

    return wrapper
