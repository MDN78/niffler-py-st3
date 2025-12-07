import requests
import allure

from models.spend import SpendAdd, Spend
from tools.sessions import BaseSession
from models.config import Envs


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
        return Spend.model_validate(response.json())

    @allure.step('HTTP: get spends')
    def get_spends(self) -> list[Spend]:
        response = self.session.get("/api/spends/all")
        return [Spend.model_validate(item) for item in response.json()]

    @allure.step('HTTP: remove spends')
    def remove_spends(self, ids: list[str]) -> None:
        response = self.session.delete("/api/spends/remove", params={"ids": ids})

    @allure.step('HTTP: update spends')
    def update_spend(self, update: Spend) -> Spend:
        response = self.session.patch("/api/spends/edit", data=update.model_dump_json())
        return Spend.model_validate(response.json())
