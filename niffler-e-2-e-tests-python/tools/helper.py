from playwright.sync_api import Page


def check_category_in_db(response, username: str, test_category: str):
    first_category = response[0]
    assert first_category.username == username
    assert first_category.name == test_category


def check_spend_in_db(response, amount: float, category_name: str, description: str, username: str):
    for spend, category in response:
        assert description == spend.description
        assert username == spend.username
        assert amount == spend.amount
        assert category_name == category.name


def delete_category_in_db(response, spend_db):
    for item in response:
        spend_sql_obj = item[0]
        category_id = spend_sql_obj.category_id
        spend_db.delete_category(category_id)


def mock_static_resources(page: Page):
    """
    Метод отключения подгрузки статических файлов
    """
    page.route("**/*.{ico,png,jpg,webp,mp3,mp4,woff,woff2}", lambda route: route.abort())
