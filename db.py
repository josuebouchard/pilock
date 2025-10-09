from contextlib import contextmanager
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

# Private variable initializing the engine
_engine = create_engine("sqlite:///database.db")


# Dependency function to access DB
def _get_session_dep():
    with Session(_engine) as session:
        yield session


@contextmanager
def get_session():
    with Session(_engine) as session:
        yield session


# Dependency annotation
SessionDep = Annotated[Session, Depends(_get_session_dep)]


def create_db_and_tables():
    """Recreates database schema"""
    SQLModel.metadata.create_all(_engine)


# For `from db import *`
__all__ = ["SessionDep", "create_db_and_tables"]
