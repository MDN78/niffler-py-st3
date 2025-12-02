from abc import ABC, abstractmethod
import allure
from playwright.sync_api import Locator, Page, expect
from tools.logger import get_logger

logger = get_logger("BASE_COMPONENT")


class Component(ABC):
    def __init__(self, page: Page, locator: str, name: str) -> None:
        self.page = page
        self.name = name
        self.locator = locator

    @property
    @abstractmethod
    def type_of(self) -> str:
        return 'component'

    def get_locator(self, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        step = f'Getting locator name: "{locator}"'
        with allure.step(step):
            logger.info(step)
            return self.page.locator(locator)

    def click(self, **kwargs) -> None:
        step = f'Clicking {self.type_of} with name "{self.name}"'
        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(**kwargs)
            locator.click()

    def should_be_visible(self, **kwargs) -> None:
        step = f'Checking that {self.type_of} "{self.name}" is visible'
        with allure.step(step):
            locator = self.get_locator(**kwargs)
            logger.info(step)
            expect(locator).to_be_visible()

    def should_have_text(self, text: str, **kwargs) -> None:
        step = f'Checking that {self.type_of} "{self.name}" has text "{text}"'
        with allure.step(step):
            locator = self.get_locator(**kwargs)
            logger.info(step)
            expect(locator).to_have_text(text)
