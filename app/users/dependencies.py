from typing import Annotated
from fastapi import Depends
from .repository import UserRepository
from db import SessionDep


def _get_user_repo(session: SessionDep):
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(_get_user_repo)]
