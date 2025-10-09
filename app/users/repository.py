from sqlmodel import Session, select, col

from .tables import UserModel
from .user import User

# === Repositories


class UserRepository:
    _session: Session

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_users(self, limit: int = 20, start: int = 0):
        stmt = select(UserModel).where(col(UserModel.id) >= start).limit(limit)
        db_users = self._session.exec(stmt)

        return [UserRepository._to_domain(db_user) for db_user in db_users]

    def get_user(self, id: str):
        db_user = self._session.get(UserModel, id)
        if db_user is None:
            return None

        return UserRepository._to_domain(db_user)

    # === Helpers ===

    @staticmethod
    def _to_domain(db_user: UserModel) -> User:
        assert db_user.id is not None
        return User(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            email=db_user.email,
        )
