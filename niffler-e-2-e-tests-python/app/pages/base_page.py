from playwright.sync_api import Page, Response
import allure
from tools.logger import get_logger

logger = get_logger("BASE PAGE")


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step('UI: open page')
    def visit(self, url: str) -> Response | None:
        logger.info(f'Visit {url}')
        return self.page.goto(url, wait_until='networkidle')

    @allure.step('UI: reload page')
    def reload(self) -> Response | None:
        return self.page.reload(wait_until='domcontentloaded')

    @allure.step('UI: waiting for loading page')
    def wait_for_load(self):
        self.page.wait_for_load_state("domcontentloaded")
