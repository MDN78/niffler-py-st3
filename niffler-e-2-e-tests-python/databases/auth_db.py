import allure

from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select
from allure_commons.types import AttachmentType

from models.auth import User
from models.config import Envs
from tools.logger import get_logger

logger = get_logger("SQL USERS AUTH")

class UserDb:
    """Класс для работы с User в базе данных"""
    engine: Engine

    def __init__(self, envs: Envs):
        self.engine = create_engine(envs.auth_db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    @allure.step('DB: attach sql')
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        logger.info(f"{name}")
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    def get_user_by_username(self, username: str) -> User | None:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            try:
                user = session.exec(statement).one()
            except Exception:
                user = None
            return user