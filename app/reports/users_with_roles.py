from enum import Enum, auto
import attrs

# === Classes ===

class UserRoles(Enum):
    WEB_USER = auto()
    TAG_USER = auto()


@attrs.define(slots=True, frozen=True)
class UserView:
    id: int = attrs.field(eq=True, hash=True)
    first_name: str = attrs.field(eq=False, hash=False)
    last_name: str = attrs.field(eq=False, hash=False)
    email: str = attrs.field(eq=False, hash=False)

    # Projection from other
    roles: frozenset[UserRoles] = attrs.field(
        factory=frozenset,
        converter=frozenset,
        eq=False,
        hash=False,
    )

# === Query

from users.tables import UserModel
from db import get_session
from sqlmodel import select

# def get_users():
#     with get_session() as session:
#         session.exec(select(UserModel).join())