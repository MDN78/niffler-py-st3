import requests
import allure

from models.category import Category, CategoryAdd
from tools.sessions import BaseSession
from models.config import Envs


class CategoryHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    @allure.step('HTTP: get categories')
    def get_categories(self) -> list[CategoryAdd]:
        response = self.session.get('/api/categories/all')
        return [CategoryAdd.model_validate(item) for item in response.json()]

    @allure.step('HTTP: add category')
    def add_category(self, category: CategoryAdd) -> Category:
        response = self.session.post("/api/categories/add", json=category.model_dump())
        return Category.model_validate(response.json())
