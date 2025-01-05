"""Test the main module."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from db import get_session
from main import app
from models import Base
from user.models import User

# Initialize the Postgres container at the module level to reuse across fixtures
postgres_container = PostgresContainer("postgres:16")


@pytest.fixture(scope="session")
def engine():
    """Start and stop the Postgres container."""
    postgres_container.start()
    engine = create_engine(postgres_container.get_connection_url())
    yield engine
    postgres_container.stop()


@pytest.fixture(scope="session")
def session(engine):
    """Create a new database session for a test."""
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Create a user for testing
    user = User(name="Alice", email="alice@alice.com")
    session.add(user)
    session.commit()

    def get_testing_session():
        """Provide a transactional scope around a series of operations."""
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = get_testing_session

    yield session


@pytest.fixture(scope="module")
def client(session):
    """Provide a TestClient that uses the overridden dependency."""
    return TestClient(app)


def test_root(client):
    """Test the root route."""
    response = client.get("/", timeout=5)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World"}


def test_create_user(client):
    """Test the create user route."""
    payload = {"name": "Dennis", "email": "Dennis@Dennis.com"}
    response = client.post("/users/", json=payload, timeout=5)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["name"] == "Dennis"
    assert data["email"] == "Dennis@Dennis.com"


def test_read_user(client):
    """Test the read user route."""
    response = client.get("/users/1", timeout=5)

    expected_response = {"id": 1, "name": "Alice", "email": "alice@alice.com", "posts": []}

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
