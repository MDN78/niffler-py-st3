from playwright.sync_api import APIResponse

from models.category import Category, CategoryAdd


class CategoryHttpClient:
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

    def get_categories(self) -> list[CategoryAdd]:
        response = self.request_context.get("/api/categories/all")
        self.raise_for_status(response)
        return [CategoryAdd.model_validate(item) for item in response.json()]

    def add_category(self, category: CategoryAdd) -> Category:
        category = CategoryAdd.model_validate(category)
        response = self.request_context.post("/api/categories/add", data=category.model_dump())
        self.raise_for_status(response)
        return Category.model_validate(response.json())

    @staticmethod
    def raise_for_status(response: APIResponse):
        if not response.ok:
            raise Exception(f"{response.status}")
