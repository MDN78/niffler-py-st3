import requests
import allure

from http import HTTPStatus
from models.spend import SpendAdd, Spend
from tools.sessions import BaseSession
from models.config import Envs
from tools.assertions.base import assert_status_code


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

    @allure.step('HTTP: add spends')
    def add_spends(self, spend: SpendAdd) -> Spend:
        response = self.session.post("/api/spends/add", json=spend.model_dump())
        assert_status_code(response.status_code, HTTPStatus.CREATED)
        return Spend.model_validate(response.json())

    @allure.step('HTTP: get spends')
    def get_spends(self) -> list[Spend]:
        response = self.session.get("/api/spends/all")
        assert_status_code(response.status_code, HTTPStatus.OK)
        return [Spend.model_validate(item) for item in response.json()]

    @allure.step('HTTP: remove spends')
    def remove_spends(self, ids: list[str]) -> None:
        response = self.session.delete("/api/spends/remove", params={"ids": ids})
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.step('HTTP: update spends')
    def update_spend(self, update: Spend) -> Spend:
        response = self.session.patch("/api/spends/edit", data=update.model_dump_json())
        assert_status_code(response.status_code, HTTPStatus.OK)
        return Spend.model_validate(response.json())

    @allure.step('HTTP: Get id all users categories')
    def get_ids_all_categories(self, exclude_archived: bool = False) -> list[str]:
        response = self.session.get('/api/categories/all', params={'archived': exclude_archived})
        return [cat['id'] for cat in response.json()]

    @allure.step('HTTP: Delete spend by ID')
    def delete_spending_by_id(self, spending_id: str) -> int:
        response = self.session.delete(f'/api/spends/remove?ids={spending_id}')
        return response.status_code

    @allure.step('HTTP: Get ID all users spends')
    def get_ids_all_spending(self) -> list[str]:
        ids = []
        for currency in ['RUB', 'KZT', 'USD', 'EUR']:
            response = self.session.get(f'/api/spends/all?filterCurrency={currency}')
            body = response.json()
            ids += [spend['id'] for spend in body]
        return ids
