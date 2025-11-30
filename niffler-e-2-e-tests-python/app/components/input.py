from playwright.sync_api import expect

from app.components.base_component import Component


class Input(Component):
    @property
    def type_of(self) -> str:
        return 'input'

    def fill(self, value: str, validate_value=False, **kwargs):
        locator = self.get_locator(**kwargs)
        locator.fill(value)

        if validate_value:
            self.should_have_value(value, **kwargs)

    def clear(self, validate_empty=False, **kwargs):
        """Очищает поле ввода"""
        locator = self.get_locator(**kwargs)
        locator.clear()

        if validate_empty:
            self.should_be_empty(**kwargs)

    def should_be_empty(self, **kwargs):
        """Проверяет, что поле пустое"""
        locator = self.get_locator(**kwargs)
        expect(locator).to_have_value("")

    def should_have_value(self, value: str, **kwargs):
        locator = self.get_locator(**kwargs)
        expect(locator).to_have_value(value)
