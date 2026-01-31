from jinja2 import Environment, select_autoescape, FileSystemLoader
from tools.logger import get_logger

logger = get_logger("TEMPLATES XML READER")


def current_user_xml(username: str) -> str:
    logger.info(f"Read template for User: {username}")
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('resources/templates/current_user.xml')
    return template.render({'username': username})
