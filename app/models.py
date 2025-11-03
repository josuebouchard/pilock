from typing import Any
from sqlmodel import Column, SQLModel, Field, DateTime
from datetime import UTC, datetime


class PersonInformation(SQLModel):
    org_id: str
    first_name: str
    last_name: str


class _TagBase(PersonInformation):
    # TODO: should only hold UPPERCASE characters
    # TODO: should only accept "hex-strings"
    tag_uid: str


class Tag(_TagBase, table=True):
    __tablename__: Any = "tags"  # pyright: ignore[reportExplicitAny]

    id: int | None = Field(default=None, primary_key=True)


class TagEdit(_TagBase):
    pass


class AccessLog(SQLModel, table=True):
    __tablename__: Any = "access_logs"  # pyright: ignore[reportExplicitAny]

    id: int | None = Field(default=None, primary_key=True)
    tag_uid: str
    access_was_granted: bool
    timestamp: datetime | None = Field(default_factory=lambda: datetime.now(UTC))

    org_id: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
