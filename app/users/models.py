from typing import Any, override

from sqlmodel import Field, Session, SQLModel, col, select

# === Repository ===


def get_users(session: Session, limit: int = 20, start: int = 0):
    stmt = select(User).where(col(User.id) >= start).limit(limit)
    return session.exec(stmt).all()


def get_user(session: Session, id: int):
    return session.get(User, id)


# === Models ===


class User(SQLModel, table=True):
    __tablename__: Any = "users"  # pyright: ignore[reportExplicitAny]
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str

    def sortable_name(self):
        return f"{self.last_name}, {self.first_name}"

    @override
    def __eq__(self, other: object):
        if isinstance(other, self.__class__):
            return self.id is not None and other.id is not None and self.id == other.id
        return NotImplemented
