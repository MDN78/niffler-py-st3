from playwright.sync_api import APIResponse

from models.spend import SpendAdd, Spend


class SpendsHttpClient:
    base_url: str

    def __init__(self, base_url: str, token: str, playwright):
        self.base_url = base_url
        self.request_context = playwright.request.new_context(
            base_url=base_url,
            extra_http_headers={
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

    def add_spends(self, spend: SpendAdd) -> Spend:
        spend_data = SpendAdd.model_validate(spend)
        response = self.request_context.post("/api/spends/add", data=spend_data.model_dump())
        self.raise_for_status(response)
        return Spend.model_validate(response.json())

    def get_spends(self) -> list[Spend]:
        response = self.request_context.get("/api/v2/spends/all")
        self.raise_for_status(response)
        return [Spend.model_validate(item) for item in response.json()["content"]]

    def remove_spends(self, ids: list[str]) -> None:
        ids_param = ",".join(ids)
        response = self.request_context.delete("/api/spends/remove", params={"ids": ids_param})
        self.raise_for_status(response)

    @staticmethod
    def raise_for_status(response: APIResponse):
        if not response.ok:
            raise Exception(f"{response.status}")
