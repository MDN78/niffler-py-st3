import pytest


class Pages:
    """Набор фикстур для различных типов тестов"""
    profile_page = pytest.mark.usefixtures("profile_page")
    open_login_page = pytest.mark.usefixtures("open_login_page")
    open_profile_page = pytest.mark.usefixtures("open_profile_page")
    open_spend_page = pytest.mark.usefixtures("open_spend_page")


class TestData:
    """Класс набор фикстур параметризации тестов"""
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param.description)
    category_db = lambda x: pytest.mark.parametrize("category_db", [x], indirect=True, ids=lambda param: param.name)
