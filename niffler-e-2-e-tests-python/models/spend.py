from datetime import datetime
from pydantic import BaseModel

from models.category import CategoryAdd, Category
from sqlmodel import Field, SQLModel


class Spend(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: Category
    spendDate: datetime
    currency: str
    username: str


class SpendAdd(BaseModel):
    amount: float
    description: str
    category: CategoryAdd
    spendDate: str
    currency: str


# class SpendSQL(SQLModel, table=True):
#     __tablename__ = 'spend'
#     id: str | None = Field(default=None, primary_key=True)
#     username: str
#     amount: float
#     description: str
#     category_id: str = Field(foreign_key="category.id")
#     spend_date: datetime
#     currency: str