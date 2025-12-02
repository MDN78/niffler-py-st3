# from playwright.sync_api import APIResponse
#
# from models.spend import SpendAdd, Spend
#
#
# class SpendsHttpClient:
#     base_url: str
#
#     def __init__(self, base_url: str, token: str, playwright):
#         self.base_url = base_url
#         self.request_context = playwright.request.new_context(
#             base_url=base_url,
#             extra_http_headers={
#                 'Accept': 'application/json',
#                 'Authorization': f'Bearer {token}',
#                 'Content-Type': 'application/json'
#             }
#         )
#
#     def add_spends(self, spend: SpendAdd) -> Spend:
#         spend_data = SpendAdd.model_validate(spend)
#         response = self.request_context.post("/api/spends/add", data=spend_data.model_dump())
#         self.raise_for_status(response)
#         return Spend.model_validate(response.json())
#
#     def get_spends(self) -> list[Spend]:
#         response = self.request_context.get("/api/v2/spends/all")
#         self.raise_for_status(response)
#         return [Spend.model_validate(item) for item in response.json()["content"]]
#
#     def remove_spends(self, ids: list[str]) -> None:
#         ids_param = ",".join(ids)
#         response = self.request_context.delete("/api/spends/remove", params={"ids": ids_param})
#         self.raise_for_status(response)
#
#     @staticmethod
#     def raise_for_status(response: APIResponse):
#         if not response.ok:
#             raise Exception(f"{response.status}")


import requests
from urllib.parse import urljoin

from models.spend import SpendAdd, Spend


class SpendsHttpClient:
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

    def add_spends(self, spend: SpendAdd) -> Spend:
        url = urljoin(self.base_url, "/api/spends/add")
        response = self.session.post(url, json=spend.model_dump())
        self.raise_for_status(response)
        return Spend.model_validate(response.json())

    def get_spends(self) -> list[Spend]:
        response = self.session.get(urljoin(self.base_url, '/api/spends/all'))
        self.raise_for_status(response)
        return [Spend.model_validate(item) for item in response.json()]

    def remove_spends(self, ids: list[str]) -> None:
        url = urljoin(self.base_url, "/api/spends/remove")
        response = self.session.delete(url, params={"ids": ids})
        self.raise_for_status(response)

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise