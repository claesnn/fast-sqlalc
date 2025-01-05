"""Services for the post module."""

from db import SessionDep
from post.models import Post, PostCreate
from user.models import User, UserCreate


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
    user_data = payload.model_dump()
    posts_data = user_data.pop("posts", [])

    user = User(**user_data)
    user.posts = [Post(**post_data) for post_data in posts_data]

    session.add(user)
    session.commit()

    return user


def get_user(session: SessionDep, user_id: int):
    """Get a user."""
    return session.get(User, user_id)


def list_users(session: SessionDep):
    """List all users."""
    return session.query(User).all()
