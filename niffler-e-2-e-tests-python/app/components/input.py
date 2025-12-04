from playwright.sync_api import expect
import allure
from app.components.base_component import Component
from tools.logger import get_logger

logger = get_logger("INPUT")


class Input(Component):
    @property
    def type_of(self) -> str:
        return 'input'

    def fill(self, value: str, validate_value=False, **kwargs):
        step = f'Fill {self.type_of} "{self.name}" to value "{value}"'
        with allure.step(step):
            locator = self.get_locator(**kwargs)
            logger.info(step)
            locator.fill(value)

            if validate_value:
                self.should_have_value(value, **kwargs)

    def clear(self, validate_empty=False, **kwargs):
        """Очищает поле ввода"""
        step = f'Prepare {self.type_of} "{self.name}" for adding new name"'
        with allure.step(step):
            locator = self.get_locator(**kwargs)
            logger.info(step)
            locator.clear()

            if validate_empty:
                self.should_be_empty(**kwargs)

    def should_be_empty(self, **kwargs):
        """Проверяет, что поле пустое"""
        step = f'Checking that {self.type_of} "{self.name}" is empty"'
        with allure.step(step):
            locator = self.get_locator(**kwargs)
            logger.info(step)
            expect(locator).to_have_value("")

    def should_have_value(self, value: str, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" has a value "{value}"'
        with allure.step(step):
            locator = self.get_locator(**kwargs)
            logger.info(step)
            expect(locator).to_have_value(value)
