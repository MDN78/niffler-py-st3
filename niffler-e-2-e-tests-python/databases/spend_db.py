from collections.abc import Sequence

import allure
from allure_commons.types import AttachmentType

from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select, delete

from models.category import Category
from models.spend import SpendSQL
from tools.logger import get_logger

logger = get_logger("SQL DATABASE")


class SpendDb:
    """Класс для работы с тратами в базе данных"""
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    @allure.step('DB: attach sql')
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        logger.info(f"{statement_with_params} {name}")
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    @allure.step('DB: get user {username} categories')
    def get_user_categories(self, username: str) -> Sequence[Category]:
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            return session.exec(statement).all()

    @allure.step('DB: delete category by ID {category_id}')
    def delete_category(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            session.delete(category)
            session.commit()

    @allure.step('DB: get user category by id {category_id}')
    def get_user_category(self, category_id: str):
        with Session(self.engine) as session:
            statement = select(Category).where(Category.id == category_id)
            return session.exec(statement).first()

    @allure.step('DB: get user spends by ID {spend_id}')
    def get_spend_by_id(self, spend_id: str) -> SpendSQL:
        with Session(self.engine) as session:
            statement = select(SpendSQL).where(SpendSQL.id == spend_id)
            return session.exec(statement).first()

    @allure.step('DB: get user spends {username}')
    def get_user_spends(self, username: str):
        with Session(self.engine) as session:
            statement = select(SpendSQL, Category).join(Category, SpendSQL.category_id == Category.id).where(
                SpendSQL.username == username)
            result = session.exec(statement).all()
            return result

    @allure.step("DB delete all spends users {username}")
    def delete_spends_by_user(self, username: str):
        with Session(self.engine) as session:
            statement = delete(SpendSQL).where(SpendSQL.username == username)
            session.exec(statement)
            session.commit()
