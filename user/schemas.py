"""Extra schemas for User."""

from post.models import PostCreate, PostRead

from .models import UserCreate, UserRead


class UserReadWithPosts(UserRead):
    """Schema for a full User."""

    posts: list[PostRead]


class UserCreateWithPosts(UserCreate):
    """Schema for creating a User with Posts."""

    posts: list[PostCreate] = []
