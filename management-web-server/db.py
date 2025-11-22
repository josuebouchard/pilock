from contextlib import contextmanager
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Private variable initializing the engine
_engine = create_engine("sqlite:///database.db")


# Dependency function to access DB
def _get_session_aux():
    with Session(_engine) as session:
        yield session


get_session = contextmanager(_get_session_aux)

# Dependency annotation
SessionDep = Annotated[Session, Depends(_get_session_aux)]


def create_db_and_tables():
    """Recreates database schema"""
    SQLModel.metadata.create_all(_engine)


# For `from db import *`
__all__ = ["SessionDep", "create_db_and_tables"]
