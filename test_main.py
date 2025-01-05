"""Test the main module."""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from db import get_session
from main import app
from models import Base

client = TestClient(app)


sqlite_file_name = ":memory:"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
testing_engine = create_engine(sqlite_url, connect_args=connect_args, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=testing_engine)


def get_testing_session():
    """Get a new testing session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = get_testing_session


def setup_module(module):
    """Set up the test database before any tests run."""
    Base.metadata.create_all(bind=testing_engine)


def teardown_module(module):
    """Tear down the test database after all tests run."""
    Base.metadata.drop_all(bind=testing_engine)


def test_root():
    """Test the root route."""
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World"}


def test_create_user():
    """Test the create user route."""
    payload = {"name": "Alice", "email": "alice@alice.com"}
    response = client.post("/users/", json=payload)

    payload["id"] = 1
    payload["posts"] = []

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == payload


def test_read_user():
    """Test the read user route."""
    response = client.get("/users/1")

    payload = {"id": 1, "name": "Alice", "email": "alice@alice.com", "posts": []}

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == payload
