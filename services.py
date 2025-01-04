"""Services for the post module."""

from db import SessionDep
from models import Post, User
from schemas import PostCreate, UserCreate


def create_post(session: SessionDep, payload: PostCreate, user_id: int):
    """Create a post."""
    post = Post(**payload.model_dump(), user_id=user_id)
    session.add(post)
    session.commit()
    return post


def get_post(session: SessionDep, post_id: int):
    """Get a post."""
    return session.get(Post, post_id)


def list_posts(session: SessionDep):
    """List all posts."""
    return session.query(Post).all()


def create_user(session: SessionDep, payload: UserCreate):
    """Create a user."""
    user = User(**payload.model_dump())
    session.add(user)
    session.commit()
    return user


def get_user(session: SessionDep, user_id: int):
    """Get a user."""
    return session.get(User, user_id)


def list_users(session: SessionDep):
    """List all users."""
    return session.query(User).all()
