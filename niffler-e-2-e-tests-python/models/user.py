from pydantic import BaseModel
from sqlalchemy import MetaData
from sqlmodel import SQLModel, Field


class UserName(BaseModel):
    username: str


class User(SQLModel, table=True):
    metadata = MetaData()
    id: str = Field(default=None, primary_key=True)
    username: str
    currency: str = "RUB"
    firstname: str
    surname: str
    currency: str
    photo: str | None = None
    photo_small: str | None = None
    full_name: str
    __table_args__ = {"extend_existing": True}
