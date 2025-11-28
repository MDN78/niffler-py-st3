import requests
from urllib.parse import urljoin

from models.category import Category, CategoryAdd


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

    def get_categories(self) -> list[CategoryAdd]:
        response = self.session.get(urljoin(self.base_url, '/api/categories/all'))
        self.raise_for_status(response)
        return [CategoryAdd.model_validate(item) for item in response.json()]

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
