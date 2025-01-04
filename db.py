"""Database configuration and session management."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    """Create the database and tables."""
    MetaData.create_all(engine)


def get_session():
    """Get a new session."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
