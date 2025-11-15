from selene import browser


class BasePage:
    """Класс взаимодействия с главной страницей приложения"""

    def open_url(self, url: str) -> None:
        browser.open(url)
