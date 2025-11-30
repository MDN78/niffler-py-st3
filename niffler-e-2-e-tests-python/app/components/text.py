from app.components.base_component import Component


class Text(Component):
    @property
    def type_of(self):
        return 'text'