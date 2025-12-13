import allure
from app.components.base_component import Component
from tools.logger import get_logger

logger = get_logger("BUTTON")


class Button(Component):
    @property
    def type_of(self) -> str:
        return 'button'

    def click(self, **kwargs) -> None:
        step = f'Clicking {self.type_of} with name "{self.name}"'
        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(**kwargs)
            locator.click()

    def hover(self, **kwargs) -> None:
        with allure.step(f'Hovering over {self.type_of} with name "{self.name}"'):
            locator = self.get_locator(**kwargs)
            locator.hover()

    def double_click(self, **kwargs):
        with allure.step(f'Double clicking {self.type_of} with name "{self.name}"'):
            locator = self.get_locator(**kwargs)
            locator.dblclick()
