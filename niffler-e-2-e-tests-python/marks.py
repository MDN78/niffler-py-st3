import pytest


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    main_page_late = pytest.mark.usefixtures("main_page_late")
    profile_page = pytest.mark.usefixtures("profile_page")
    login_page = pytest.mark.usefixtures("login_page")


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param["description"])
