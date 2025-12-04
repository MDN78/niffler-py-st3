import requests
from urllib.parse import urljoin
import allure
from requests import Response
from requests_toolbelt.utils.dump import dump_response
from allure_commons.types import AttachmentType

from models.category import Category, CategoryAdd
from tools.logger import get_logger

logger = get_logger("CATEGORY CLIENT")


class CategoryHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })
        self.session.hooks["response"].append(self.attach_response)

    @staticmethod
    @allure.step('HTTP: attach response')
    def attach_response(response: Response, *args, **kwargs):
        attachment_name = response.request.method + " " + response.request.url
        logger.info(f"API: method and url: {attachment_name}")
        allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

    @allure.step('HTTP: get categories')
    def get_categories(self) -> list[CategoryAdd]:
        response = self.session.get(urljoin(self.base_url, '/api/categories/all'))
        self.raise_for_status(response)
        return [CategoryAdd.model_validate(item) for item in response.json()]

    @allure.step('HTTP: add category')
    def add_category(self, category: CategoryAdd) -> Category:
        response = self.session.post(urljoin(self.base_url, "/api/categories/add"), json=category.model_dump())
        self.raise_for_status(response)
        return Category.model_validate(response.json())

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise
