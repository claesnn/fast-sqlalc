"""Extra schemas for User."""

from post.models import PostRead

from .models import UserRead


class UserFull(UserRead):
    """Schema for a full User."""

    posts: list[PostRead]
