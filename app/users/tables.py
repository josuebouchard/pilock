from typing import Any
from sqlmodel import SQLModel, Field


class UserModel(SQLModel, table=True):
    __tablename__: Any = "users"  # pyright: ignore[reportExplicitAny]
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
